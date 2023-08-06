# Import the necessary classes
from transformers import (
    AutoTokenizer, # Converts text to tokens and vice versa for the model to understand
    AutoModelForCausalLM, # Model that generates text from a prompt
    TextStreamer, # Print what the model generates as it generates it
)

# Define the default arguments
DEFAULT_MODEL_NAME = "Fredithefish/ScarletPajama-3B-HF" # https://huggingface.co/Fredithefish/ScarletPajama-3B-HF
DEFAULT_PROMPT = "THE END IS NEVER THE END IS NEVER " # https://thestanleyparable.fandom.com/wiki/The_End_Is_Never...
DEFAULT_MAX_MEMORY_RATIO = 0.5 # Randomly chosen


# Define the main function
def isnever(
    model_name=DEFAULT_MODEL_NAME, # Model to generate text with, more info here: https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModelForCausalLM
    prompt=DEFAULT_PROMPT, # Initial prompt for model, length (in tokens) < the model's max_length
    max_memory_ratio=DEFAULT_MAX_MEMORY_RATIO, # % of past tokens to remember, 0 < x < 1
    **kwargs # Parameters for the model.generate() function, more info here: https://huggingface.co/docs/transformers/generation_strategies#text-generation-strategies
):
    # Check if the arguments are valid
    if (
        not model_name or type(model_name) != str
    ):  # If no model is provided or if the model is not a string
        model_name = DEFAULT_MODEL_NAME  # Use the default model
    if (
        not prompt or type(prompt) != str
    ):
        prompt = DEFAULT_PROMPT
    if (
        not max_memory_ratio
        or type(max_memory_ratio) != float
        or type(max_memory_ratio) != int
        or max_memory_ratio <= 0
        or max_memory_ratio >= 1
    ):
        max_memory_ratio = DEFAULT_MAX_MEMORY_RATIO
        
    # Download model and tokenizer, where retries are used to catch invalid model names/model download errors
    while True:
        try:
            # Setup the model
            model = AutoModelForCausalLM.from_pretrained(
                model_name
            )
            tokenizer = AutoTokenizer.from_pretrained(
                model_name
            )
            streamer = TextStreamer(
                tokenizer,
                skip_prompt=True,  # To skip the prompt when streaming since it's already printed
            )
            break
        except OSError:  # To catch invalid model names
            model_name = DEFAULT_MODEL_NAME  # To use the default model
            continue  # To ignore any errors and try again
        except Exception:  # To catch model download errors
            continue  # To ignore any errors and try again

    # Define model.generate() arguments
    max_length = model.config.max_length  # Context window size of the model (in tokens)
    max_memory = (
        int(max_length * max_memory_ratio) + 1
    )  # Add 1 to avoid empty prompt

    # Check if prompt is too long
    inputs = tokenizer(
        [
            prompt
        ],  # Wrap prompt as a list since inputs are usually a batch
        return_tensors="pt",  # Return PyTorch tensors
    )['input_ids'][0] # Text to tokens, index 0 because only one prompt
    if len(inputs) >= max_length: # If the prompt is too long
        inputs = inputs[:max_length - 1] # Only keep the first max_length - 1 tokens (- 1 to give model space to generate)
        prompt = tokenizer.decode(
            inputs,
            skip_special_tokens=True,  # To remove special tokens like <eos>
        )  # Tokens to text
    print(prompt)  # Print the initial prompt since it's not streamed
    
    # Set up the conversation loop, where the response is used as the next prompt
    while True:
        inputs = tokenizer(
            [
                prompt
            ],  # Wrap prompt as a list since inputs are usually a batch
            return_tensors="pt",
        )
        response = model.generate(
            **inputs,  # Unpack dictionary into keyword arguments
            streamer=streamer,
            max_length=max_length,
            num_return_sequences=1,  # To return only one response
            pad_token_id=tokenizer.eos_token_id,  # To remove warning message in console
            **kwargs,  # Unpack dictionary into keyword arguments
        )
        prompt = tokenizer.decode(
            response[0][
                -max_memory:
            ], # index 0 since inputs are usually a batch
            skip_special_tokens=True,
        )


# Run the function for testing
# Arguments from here: https://huggingface.co/docs/transformers/generation_strategies#multinomial-sampling
# isnever(
#     do_sample=True,
#     num_beams=1,
# )
