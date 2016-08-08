##############################################################################
# The Edge of Mists schedule
#
# Script for EOM shedule events

label shd_evn_None_template(character):
    $ d = character.description()
    '[d] TOASTED!'
    return