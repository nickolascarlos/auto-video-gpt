import openai, json

# Creates content to videos by using OpenAI text completition API
class OpenAIContentFactory:

    def __init__(self, arguments):
        if not arguments['api_key']:
            raise 'OpenAIContentFactory requires an API key'
        openai.api_key = arguments['api_key']

    #
    # This method receives a subject and a gpt_prompt as parameters.
    # The gpt_prompt must be a prompt that describes, also,
    # the schema of the response, like an array of values
    # or a JSON and its schema.
    #
    # [!] The expected schema is defined by the Coordinator.
    #
    # [!] Since it's not guaranteed the GPT response follows the
    # requested schema, it's a good idea to validate the output
    # of this function before further use.
    #
    # TODO: Implement a schema validator
    #
    def get_content(self, subject, gpt_prompt):
        prompt = gpt_prompt.replace('{{SUBJECT}}', subject)

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.40,
            max_tokens=3000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return json.loads(response['choices'][0]['text'])
