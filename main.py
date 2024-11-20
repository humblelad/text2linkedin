import requests
import json
import re

def image_share(access_token, image_path, post_text):

  """Shares an image on LinkedIn using the LinkedIn API.

  Args:
    access_token: A valid LinkedIn API access token.
    image_path: The path to the image file to share.
    post_text: The text of the post to accompany the image.

  Returns:
    A boolean indicating whether the image was shared successfully.
  """

  # Initialize the upload.
  headers = {
    'Authorization':f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }
  data = {
    'registerUploadRequest': {
      'recipes': ['urn:li:digitalmediaRecipe:feedshare-image'],
      'owner': 'urn:li:person:Er9iNHQT8p',
      'serviceRelationships': [
        {
          'relationshipType': 'OWNER',
          'identifier': 'urn:li:userGeneratedContent'
        }
      ]
    }
  }

  response = requests.post('https://api.linkedin.com/v2/assets?action=registerUpload', headers=headers, data=json.dumps(data))

  # Upload the image.
  upload_url = \
  response.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']

  # Determine the appropriate Content-Type based on the image format
  if image_path.endswith('.jpg') or image_path.endswith('.jpeg'):
    content_type = 'image/jpeg'
  elif image_path.endswith('.png'):
    content_type = 'image/png'
  else:
    # If you don't know the format, you can use a generic binary type
    content_type = 'application/octet-stream'

  headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': content_type  # Set the appropriate content type
  }

  print(upload_url)

  my_media=response.json()['value']['asset']
  print(my_media)

  with open(image_path, 'rb') as image_file:
    image_data = image_file.read()

    response = requests.post(upload_url, headers=headers, data=image_data)

  # Share the image.
  headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }
  data = {

      "author": "urn:li:person:Er9iNHQT8p",
      "lifecycleState": "PUBLISHED",
      "specificContent": {
        "com.linkedin.ugc.ShareContent": {
          "shareCommentary": {
            "text":post_text
          },
          "shareMediaCategory": "IMAGE",
          "media": [
            {
              "status": "READY",
              "description": {
                "text": "Center stage!"
              },
              "media": my_media,
              "title": {
                "text": "LinkedIn Talent Connect 2021"
              }
            }
          ]
        }
      },
      "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
      }

  }
  response = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, data=json.dumps(data))
  print(data)
  if response.status_code == 201:
    return True
  else:
    return False

# Example usage:


# Open the file for reading
with open("configure.txt", "r") as f:
    # Read the entire file into a string
    file_contents = f.read()

# Extract the value within `test=`
img = re.search(r"img\s*=\s*(.*)", file_contents)
if img is not None:
    img = img.group(1)
print(img)


txt = re.search(r'txt="([^"]*)"', file_contents)
if txt is not None:

    txt = txt.group(1).strip()
    txt = txt.replace("\\n", "\n")

print(txt)




access_token = 'linkedin_api_key'

success = image_share(access_token, img, txt)
if success:
  print('Image shared successfully!')
else:
  print('Failed to share image.')
