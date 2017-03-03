label lbl_shift_relations(relations_shift):
    call screen sc_shift_relations(relations_shift)
    return


screen sc_shift_relations(relations_shift):
    
    window:
        xfill True
        yfill True
        style 'char_info_window'

        hbox:
            spacing 5
            vbox:
                imagebutton:
                    idle relations_shift.left_card()
                    action [If(relations_shift.is_left_active(), Function(relations_shift.act_left),
                            false=NullAction()), SensitiveIf(relations_shift.is_left_active()), Return()]
                text relations_shift.left_text():
                    xalign 0.5
            vbox:
                imagebutton:
                    idle relations_shift.middle_card()
                    action Function(relations_shift.act_middle), Return()
                text relations_shift.middle_text():
                    xalign 0.5
            vbox:
                imagebutton:
                    idle relations_shift.right_card()
                    action [If(relations_shift.is_right_active(), Function(relations_shift.act_right),
                            false=NullAction()), SensitiveIf(relations_shift.is_right_active()), Return()]
                text relations_shift.right_text():
                    xalign 0.5