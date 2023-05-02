import openai, json

# Creates content to videos by using OpenAI text completition API
class GPTContentFactory:

    def __init__(self, api_key):
        openai.api_key = api_key

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
    def getContent(self, subject, gpt_prompt):
        return """[
{
"title": "Colonization of Brazil",
"content": "Portuguese explorers arrived in Brazil in 1500, establishing a colony that lasted until 1822.",
"image": "Portuguese ships landing on Brazilian coast."
},
{
"title": "Slavery in Brazil",
"content": "Brazil was the largest importer of enslaved Africans, with over 4 million brought to the country from the 16th to 19th centuries.",
"image": "African slaves being sold in a Brazilian market."
},
{
"title": "Independence from Portugal",
"content": "In 1822, Brazil declared independence from Portugal and became a constitutional monarchy.",
"image": "Brazilian independence declaration ceremony."
},
{
"title": "Coffee Boom",
"content": "The late 19th century saw Brazil become the world's largest coffee producer, fueling economic growth and modernization.",
"image": "Coffee plantations in Brazil's countryside."
},
{
"title": "Military Rule",
"content": "From 1964 to 1985, Brazil was ruled by a military dictatorship that suppressed political opposition and civil liberties.",
"image": "Military personnel and tanks patrolling Brazilian streets."
},
{
"title": "Recent Developments",
"content": "Since the return to democracy in 1985, Brazil has become a major player on the global stage, but continues to struggle with economic inequality and political corruption.",
"image": "A panoramic view of Rio de Janeiro's skyline."
}
]"""
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
