if button_clicked:
            if image_rect.x < target_x:
                image_rect.x += speed
            if image_rect.y < target_y:
                image_rect.y += speed

            # Check if the image has reached the target position
            if image_rect.x >= target_x and image_rect.y >= target_y:
                image_visible = False
                button_clicked = False