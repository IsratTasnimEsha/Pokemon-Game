or j in range(2):
                        button_x = attack_choose_button_x_start2 + j * (attack_choose_button_width + attack_choose_button_spacing)
                        button_y = attack_choose_button_y_start2 + i * (attack_choose_button_height + attack_choose_button_spacing)

                        if button_x <= mouse_x <= button_x + attack_choose_button_width and button_y <= mouse_y <= button_y + attack_choose_button_height:
                            current_attack_choose_button_clicked2 = i * 2 + j
                            print("Clicked button:", current_attack_choose_button_clicked2)