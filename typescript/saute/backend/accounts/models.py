from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image, ImageDraw
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            img = Image.open(self.profile_image.path)

            # Resize the image
            img = img.resize((128, 128), Image.ANTIALIAS)

            # Convert image to a circle
            width, height = img.size
            radius = min(width, height) // 2
            circle_image = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(circle_image)
            draw.ellipse(
                (
                    width // 2 - radius,
                    height // 2 - radius,
                    width // 2 + radius,
                    height // 2 + radius,
                ),
                fill=255,
            )
            img.putalpha(circle_image)

            # Save the modified image
            output = io.BytesIO()
            img.save(output, format="PNG")
            output.seek(0)

            self.profile_image = InMemoryUploadedFile(
                output,
                "ImageField",
                f"{self.profile_image.name.split('.')[0]}.png",
                "image/png",
                len(output.getvalue()),
                None,
            )
            super().save(*args, **kwargs)
