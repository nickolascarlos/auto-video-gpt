import g4f, json

# Creates content to videos by using OpenAI text completition API
class G4FContentFactory:

    def __init__(self, arguments):
        if not arguments['model']:
            raise 'G4FContentFactory requires a model'
        self.model = arguments['model']
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
    # TODO: Uncouple prompt generation from content factories
    def getContent(self, subject, gpt_prompt):
        prompt = gpt_prompt.replace('{{SUBJECT}}', subject)

        response = g4f.ChatCompletion.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        stream=False,
                    )
        print(response)
        return response
