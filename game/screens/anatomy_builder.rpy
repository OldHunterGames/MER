init python:
    body_part = None


screen sc_anatomy_builder():
    window:
        xfill True
        yfill True
        hbox:
            frame:
                 viewport:
                    scrollbars 'vertical'
                    draggable True
                    mousewheel True
                    xsize 150
                    ysize 250
                    vbox:
                        for key, value in anatomy_features.items():
                            if value.get('basis', False):
                                textbutton value['name']:
                                    action SetVariable('body_part', BodyPart(key))
                                    if body_part is not None:
                                        selected body_part.basis.id == key
            if body_part is not None:
                for i in body_part.basis.parts:
                    frame:
                        viewport:
                            scrollbars 'vertical'
                            draggable True
                            mousewheel True
                            xsize 150
                            ysize 250
                            vbox:
                                text i
                                for key, value in anatomy_features.items():
                                    if value.get('slot') == i:
                                        textbutton value['name']:
                                            action Function(body_part.add_feature, key)
                                            if body_part.feature_by_slot(value.get('slot')) is not None:
                                                selected body_part.feature_by_slot(value.get('slot')).id == key
        if body_part is not None:
            python:
                try:
                    description = body_part.description()
                except:
                    description = 'Body part is not completed'
            text description:
                ypos 255
            textbutton "Leave":
                ypos 285
                action Return(), SetVariable('body_part', None)
