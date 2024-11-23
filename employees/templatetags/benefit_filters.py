from django.template import Library

register = Library()


@register.filter(name="capitalize_string")
def capitalize_string(string):
    result = []
    excluded_words = ["of", "an", "on", "to", "for", "and", "in", "the", "with", "a", "or"]

    for word in string.split():
        if word not in excluded_words:
            if len(word.split("-")) > 1:
                temp_result = []

                for w in word.split("-"):
                    w = w.capitalize()

                    temp_result.append(w)

                result.append("-".join(temp_result))

            else:
                result.append(word.capitalize())

        else:
            result.append(word)

    return ' '.join(result)
