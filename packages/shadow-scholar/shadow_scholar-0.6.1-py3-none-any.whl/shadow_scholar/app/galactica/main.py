import inspect
import json
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Literal, Optional

from shadow_scholar.cli import Argument, cli, safe_import

from .constants import CSS, INSTRUCTIONS

with safe_import():
    import gradio as gr

    from .galai_model import Model


class ModelWrapper:
    def __init__(
        self,
        name: str,
        precision: Literal["full", "mixed", "byte"] = "full",
        tensor_parallel: bool = False,
        logdir: Optional[str] = None,
        leftover_space: float = 0.3,
        print_to_console: bool = True,
    ):
        self.model = Model(
            name=name,
            precision=precision,
            tensor_parallel=tensor_parallel,
            leftover_space=leftover_space,
        )
        self.start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.logdir = Path(logdir) if logdir else None
        self.signature = inspect.signature(self.model.generate)
        self.print_to_console = print_to_console

    def __str__(self) -> str:
        return str(self.model) + f" start_time={self.start_time}"

    def log(self, arguments, output):
        out = {"input": arguments, "output": output}

        if self.print_to_console:
            print(json.dumps(out))

        if self.logdir is None:
            return

        self.logdir.mkdir(parents=True, exist_ok=True)

        fn = f'{self.model.name.replace("/", "_")}_{self.start_time}.jsonl'
        with open(self.logdir / fn, "a") as f:
            f.write(json.dumps(out) + "\n")

    def __call__(self, *args, **kwargs):
        arguments = self.signature.bind(*args, **kwargs).arguments

        if isinstance(opt := arguments.pop("extra_options", None), list):
            arguments["extra_options"] = {
                # evaluate strings as python literals
                k: literal_eval(v)
                for k, v in opt
                # no empty strings
                if k.strip() and v.strip()
            }

        arguments["top_k"] = (
            int(top_k) if (top_k := arguments.pop("top_k", None)) else None
        )

        arguments["top_p"] = (
            float(top_p) if (top_p := arguments.pop("top_p", None)) else None
        )

        arguments["penalty_alpha"] = (
            float(pa) if (pa := arguments.pop("penalty_alpha", None)) else None
        )

        output = self.model.generate(**arguments)
        self.log(arguments, output)
        return output


@cli(
    "app.galactica",
    arguments=[
        Argument(
            "-m",
            "--model-name",
            default="mini",
            choices=["mini", "base", "standard", "large", "huge"],
            help="Pretrained model or path to local checkpoint",
        ),
        Argument(
            "-p",
            "--server-port",
            default=7860,
            help="Port to run the server on",
        ),
        Argument(
            "-n",
            "--server-name",
            default="localhost",
            help="Server address to run the gradio app at",
        ),
        Argument(
            "-e",
            "--precision",
            default="full",
            help="Precision to use for the model",
            choices=["full", "mixed", "byte"],
        ),
        Argument(
            "-a",
            "--parallelize",
            default=False,
            action="store_true",
            help="Parallelize the model across multiple GPUs.",
        ),
        Argument(
            "-l",
            "--logdir",
            default=None,
            help="Directory to log inputs and outputs to",
        ),
        Argument(
            "-s",
            "--leftover-space",
            default=0.3,
            type=float,
            help="the amount of extra space to leave on the gpu during",
        ),
    ],
    requirements=[
        "gradio",
        "transformers",
        "torch",
        "accelerate",
        "psutil",
    ],
)
def run_galactica_demo(
    model_name: str = "mini",
    server_port: int = 7860,
    server_name: str = "localhost",
    precision: Literal["full", "mixed", "byte"] = "full",
    parallelize: bool = False,
    logdir: Optional[str] = None,
    leftover_space: float = 0.3,
):
    gl_model = ModelWrapper(
        name=model_name,
        precision=precision,
        tensor_parallel=parallelize,
        logdir=logdir,
        leftover_space=leftover_space,
    )

    with gr.Blocks(css=CSS) as demo:
        with gr.Row():
            gr.Markdown(f"# Galactica {model_name.capitalize()} Demo")
        with gr.Tab("Demo"):
            with gr.Row():
                gr.Markdown(
                    f"**Currently loaded**: {gl_model}\n\n"
                    + "Available models:\n"
                    + "\n".join(
                        f" - {k.capitalize()}: `{n}`"
                        for k, (n, _) in gl_model.model.variants.items()
                    )
                )
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(
                        lines=5, label="Input", placeholder="Prompt text"
                    )
                    submit_button = gr.Button(label="Generate")

                    max_new_tokens = gr.Number(
                        value=128,
                        label=(
                            "max_new_tokens: max number of new tokens "
                            "the model should generate"
                        ),
                    )
                    top_p = gr.Textbox(
                        value="",
                        label=(
                            "top_p: if set to float < 1, only the "
                            "smallest set of most probable tokens with "
                            "probabilities that add up to top_p or higher "
                            "are kept for generation."
                        ),
                    )
                    top_k = gr.Textbox(
                        value="",
                        label=(
                            "top_k: size of the candidate set that is "
                            "used to re-rank for contrastive search"
                        ),
                    )
                    penalty_alpha = gr.Textbox(
                        value="",
                        label=(
                            "penalty_alpha: degeneration penalty for "
                            "contrastive search"
                        ),
                    )

                    num_beams = gr.Number(
                        value=1,
                        label=(
                            "num_beams: number of beams for beam search. "
                            "1 means no beam search."
                        ),
                    )
                    num_return_sequences = gr.Number(
                        value=1,
                        label=(
                            "num_return_sequences: number of separate"
                            "computed returned sequences for each element "
                            "in the batch."
                        ),
                    )
                    return_full_text = gr.Checkbox(
                        label=(
                            "return_full_text: whether to return the full "
                            "text or just the newly generated text."
                        ),
                        value=True,
                    )
                    new_doc = gr.Checkbox(
                        label=(
                            "new_doc: whether the model should attempt "
                            "to generate a full document"
                        ),
                        value=False,
                    )
                    extra_options = gr.Dataframe(
                        label="Extra options to pass to model.generate()",
                        headers=["Parameter", "Value"],
                        col_count=2,
                        type="array",
                        interactive=True,
                    )

                with gr.Column():
                    output_text = gr.Textbox(
                        lines=25,
                        label="Output",
                        placeholder="Generated text",
                        interactive=False,
                    )

            submit_button.click(
                fn=gl_model,
                inputs=[
                    input_text,
                    max_new_tokens,
                    new_doc,
                    top_p,
                    top_k,
                    penalty_alpha,
                    num_beams,
                    num_return_sequences,
                    return_full_text,
                    extra_options,
                ],
                outputs=[output_text],
            )
        with gr.Tab("Instructions"):
            with gr.Row():
                gr.Markdown(INSTRUCTIONS, elem_id="instructions")

    try:
        demo.queue(concurrency_count=1)
        demo.launch(server_name=server_name, server_port=server_port)
    except Exception:
        sleep(1)
        gr.close_all()
