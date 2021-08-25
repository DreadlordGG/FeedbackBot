def check(m):
    return m.channel == channel and m.author.name == author
def check_y_n(m):
    return m.channel == channel and m.author.name == author and ( m.content == 'Y' or m.content == 'n' )
def check_int(m):
    return m.channel == channel and m.author.name == author and m.content.isnumeric()