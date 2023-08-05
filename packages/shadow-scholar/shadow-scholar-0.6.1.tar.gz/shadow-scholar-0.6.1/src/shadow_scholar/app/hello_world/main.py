from pathlib import Path

from shadow_scholar.cli import Argument, cli, safe_import

with safe_import():
    import gradio as gr

    # from fastapi import FastAPI
    # import uvicorn


S2R_URL = "https://www.semanticscholar.org/research/research-team"
SWS_URL = "https://github.com/allenai/shadow-scholar"
CSS_URI = Path(__file__).parent / "res" / "style.css"
IMG_URI = Path(__file__).parent / "res" / "logo.png"


@cli(
    "app.hello_world",
    arguments=[
        Argument("--host", default="localhost", help="Host to bind to"),
        Argument("--port", default=7860, type=int, help="Port to bind to"),
    ],
    requirements=["gradio"],
)
def run_hello_world(
    host: str,
    port: int,
):
    with open(CSS_URI, "r") as f:
        css = f.read()

    with gr.Blocks(title="Shadow Scholar", css=css) as app:
        gr.Markdown("# 🕶️ 🎓 Shadow Scholar 🎓 🕶️", elem_id="center")
        gr.Image(
            str(IMG_URI),
            elem_id="logo",
            shape=(400, 400),
            show_label=False,
            interactive=False,
        )
        gr.Markdown(
            "Shadow Scholar is a collection of tools and applications "
            f"from the [S2 Research Team]({S2R_URL}). To learn more about "
            f"this project, please visit our [GitHub repository]({SWS_URL}). "
            f"To install shadow scholar, run `pip install shadow-scholar`.",
            elem_id="center",
        )

    try:
        app.launch(
            server_name=host, server_port=port, show_api=False, inline=True
        )
    except Exception as e:
        app.close()
        raise e
