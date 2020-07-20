import re


def trucate_string(string, num_words_start=10, num_words_end=10):
    #n = str(int(max_words/2))
    #return re.sub(r'^(.{'+n+'}).*(.{'+n+'})$', '\g<1>...\g<2>', string)
    return string[:num_words_start] + "..." + string[-num_words_end:]