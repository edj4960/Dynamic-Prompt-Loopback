import numpy as np
from tqdm import trange

import modules.scripts as scripts
import gradio as gr

from modules import processing, shared, sd_samplers, images
from modules.processing import Processed
from modules.sd_samplers import samplers
from modules.shared import opts, cmd_opts, state

class Script(scripts.Script):
    def title(self):
        return "Dynamic Prompt Loopback"

    def show(self, is_img2img):
        return is_img2img

    def ui(self, is_img2img):
        default_loops_to_hold = gr.Slider(minimum=5, maximum=500, step=1, label="Default loops to hold prompts", value=100)
        denoising_strength_change_factor = gr.Slider(minimum=0.9, maximum=1.1, step=0.01, label='Denoising strength change factor', value=1)
        parameters = gr.Textbox(placeholder='Enter prompts in the following format Prompt 1--loops_to_hold/Prompt 2--loops_to_hold/...', lines=2, label='Parameters')
        return [default_loops_to_hold, denoising_strength_change_factor, parameters]

    def run(self, p, default_loops_to_hold, denoising_strength_change_factor, parameters):
        processing.fix_seed(p)
        batch_count = p.n_iter
        p.extra_generation_params = {
            "Denoising strength change factor": denoising_strength_change_factor,
        }

        p.batch_size = 1
        p.n_iter = 1

        parameters = parameters.split('/')
        prompts = []
        for parameter in parameters:
            param_arr = parameter.split('--')
            prompt = param_arr[0]

            loops_to_hold = default_loops_to_hold
            if len(param_arr) > 1:
                loops_to_hold = param_arr[1] 

            for j in range(0, loops_to_hold):
                prompts.append(prompt)

        prompts_len = len(prompts)

        output_images, info = None, None
        initial_seed = None
        initial_info = None

        grids = []
        all_images = []
        original_init_image = p.init_images
        state.job_count = prompts_len * batch_count

        initial_color_corrections = [processing.setup_color_correction(p.init_images[0])]
        original_prompt = p.prompt

        for n in range(batch_count):
            history = []

            # Reset to original init image at the start of each batch
            p.init_images = original_init_image

            for i, prompt in enumerate(prompts):
                p.n_iter = 1
                p.batch_size = 1
                p.do_not_save_grid = True

                if opts.img2img_color_correction:
                    p.color_corrections = initial_color_corrections

                state.job = f"Iteration {i + 1}/{prompts_len}, batch {n + 1}/{batch_count}"

                p.prompt = prompt + "," + original_prompt

                processed = processing.process_images(p)

                if initial_seed is None:
                    initial_seed = processed.seed
                    initial_info = processed.info

                init_img = processed.images[0]

                p.init_images = [init_img]
                p.seed = processed.seed + 1
                p.denoising_strength = min(max(p.denoising_strength * denoising_strength_change_factor, 0.1), 1)
                history.append(processed.images[0])

            grid = images.image_grid(history, rows=1)
            if opts.grid_save:
                images.save_image(grid, p.outpath_grids, "grid", initial_seed, p.prompt, opts.grid_format, info=info, short_filename=not opts.grid_extended_filename, grid=True, p=p)

            grids.append(grid)
            all_images += history

        if opts.return_grid:
            all_images = grids + all_images

        processed = Processed(p, all_images, initial_seed, initial_info)

        return processed
