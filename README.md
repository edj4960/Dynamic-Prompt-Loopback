# Dynamic-Prompt-Loopback
Dynamic Prompt Loopback for Stable Diffusion allows users to run loopback while setting multiple prompts that change over time.

# Purpose
The Loopback script for Stable Diffusion is a powerful tool that allows creators to generate updates to images in high iterations with ease. Dynamic Prompt Loopback builds upon this idea by allowing multiple prompts to be set allowing for automated prompt updates.

# Example - Batman to Joker

<p float="left">
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-1.png?raw=true" 
    width="150" 
  />
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-2.png?raw=true" 
    width="150" 
  />
    <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-3.png?raw=true" 
    width="150" 
  />
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-4.png?raw=true" 
    width="150" 
  />
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-5.png?raw=true" 
    width="150" 
  />
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-6.png?raw=true" 
    width="150" 
  />
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-7.png?raw=true" 
    width="150" 
  />
  <img 
    src="https://github.com/edj4960/Dynamic-Prompt-Loopback/blob/main/example_images/batman-joker-8.png?raw=true" 
    width="150" 
  />
</p>

# How to use

## Step 1 - Add the script

Place this script inside the scripts directory in stable-diffusion-webui (for information on how to setup Stable Diffusion please see [this repo](https://github.com/AUTOMATIC1111/stable-diffusion-webui).

## Step 2 - Run the script

Start Stable Diffusion and select the script in the img2img tab. Set the default for how long to hold each prompt, the denoise strength change factor, and the parameters and run.

# Options

## Default loops to hold prompt

If no loop value is set in the parameters, this value will be used to set how many loops to run a prompt.

## Denoising strength change factor

Same as in Loopback this is for updating the denoise over time. Default is 1 meaning no change.

## Parameters

Parameters are set in the following format:

Prompt 1--loops_to_hold_prompt/Prompt 2 ...

For example:

Batman, black background--50/The Joker, purple background--100

The first prompt "Batman black background" will be run for 50 loops, then the second prompt "The Joker, purple background" will be run for 100 loops. Note that loops_to_hold_prompt is optional, if not populated 'default loops to hold prompt' will be used.
