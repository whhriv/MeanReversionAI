import matplotlib.pyplot as plt
import io
import base64

# Create a sample plot
plt.figure(figsize=(14, 7))
plt.plot([1, 2, 3], [4, 5, 6], label='Test Plot')
plt.title('Test Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.legend()
plt.grid(True)

# Save plot to in-memory file
img = io.BytesIO()
plt.savefig(img, format='png')
img.seek(0)

# Encode plot to base64
img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
img_url = f'data:image/png;base64,{img_base64}'

# Print the data URL (you can test it by pasting it in a browser)
print(img_url)