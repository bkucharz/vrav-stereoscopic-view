import paraview.web.venv
from paraview import simple

from trame.app import get_server
from trame.widgets import vuetify, paraview, html, client
from trame.ui.vuetify import SinglePageLayout
from trame.ui.html import DivLayout

import os

# -----------------------------------------------------------------------------
# Trame Setup
# -----------------------------------------------------------------------------
server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ParaView Setup
# -----------------------------------------------------------------------------
disk_out_refex2 = simple.IOSSReader(
    registrationName='disk_out_ref.ex2',
    FileName=[os.path.join('examples', 'disk_out_ref.ex2')]
)
disk_out_refex2.ElementBlocks = ['block_1']
disk_out_refex2.NodeBlockFields = [
    'ash3', 'ch4', 'game3', 'h2', 'pres', 'temp', 'v']
disk_out_refex2.NodeSets = []
disk_out_refex2.SideSets = []

disk = disk_out_refex2
representation = simple.Show(disk)
view = simple.Render()

view.StereoRender = 1  # Enable stereo rendering
view.StereoType = "SplitViewportHorizontal"  # Side-by-side stereo mode

# -----------------------------------------------------------------------------
# Server State and Camera Update
# -----------------------------------------------------------------------------

# Initialize state variables for device orientation
state.alpha = 0  # Compass direction
state.beta = 0   # Tilt front/back
state.gamma = 0  # Tilt left/right


@state.change("alpha", "beta", "gamma")
def update_camera(alpha, beta, gamma, **kwargs):
    view.CameraViewUp = [0, 0, 1]
    view.CameraPosition = [0, 50, 0]
    view.CameraFocalPoint = [0, 0, 0]

    camera = view.GetActiveCamera()
    camera.Roll(360 - alpha)
    camera.Elevation(gamma)
    camera.Azimuth(beta)

    ctrl.view_update()


@ctrl.trigger("update_orientation")
def update_orientation(alpha, beta, gamma):
    alpha = round(alpha, 1)
    beta = round(beta, 1)
    gamma = round(gamma, 1)

    state.alpha = alpha
    state.beta = beta
    state.gamma = gamma
    print(f"Orientation updated: alpha={alpha}, beta={beta}, gamma={gamma}")


@ctrl.trigger("reset_orientation")
def reset_orientation():
    view.CameraViewUp = [0, 0, 1]
    view.CameraPosition = [0, 50, 0]
    view.CameraFocalPoint = [0, 0, 0]


reset_orientation()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

with DivLayout(server) as layout:

    # JavaScript to capture device orientation
    client.Script(
        """
        let lastUpdate = Date.now();

        if (window.DeviceOrientationEvent) {
            window.addEventListener("deviceorientation", (event) => {
                const now = Date.now();
                if (now - lastUpdate >= 100) {  // Wysyłanie co 100ms
                    lastUpdate = now;
                    const alpha = event.alpha || 0;
                    const beta = event.beta || 0;
                    const gamma = event.gamma || 0;

                    // console.log(`Alpha: ${alpha}, Beta: ${beta}, Gamma: ${gamma}`);
                    window.trame.state.trigger("update_orientation", [alpha, beta, gamma]);
                }
            });
        } else {
            console.error("DeviceOrientationEvent is not supported on this device.");
        }
        """
    )

    client.Script(
        """
    document.addEventListener('fullscreenchange', () => {
        if (!document.fullscreenElement) {
            document.getElementById('fullscreen-btn').style.display = 'block';
        }
    });
    """
    )

    with vuetify.VContainer(fluid=True, classes="pa-0 fill-height",  style="height: 100vh; width: 100vw; overflow: hidden;"):
        with vuetify.VBtn(
                name='fullscreen-btn',
                variant='plain',
                click="""
                    document.documentElement.requestFullscreen();
                    document.getElementById('fullscreen-btn').style.display = 'none';
                """,
                id="fullscreen-btn",
                style="""
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 10;
                width: 40px;
                height: 40px;
                opacity: 0.6;
                cursor: pointer;
                transition: opacity 0.3s;
                """
        ):
            vuetify.VIcon("mdi-fullscreen")

        html_view = paraview.VtkRemoteView(view)
        ctrl.view_update = html_view.update
        ctrl.view_reset_camera = html_view.reset_camera


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    server.start(host="0.0.0.0", port=8080)
