# instac
Tag people to a Instagram photo

## How to use
```python
import instac  

insta = instac.InstaComents('C:\\your_path\\chromedrive.exe')  
insta.following()  
insta.go_coment(link_photo="photo_url", quantity_coments=3, quantity_user_for_coment=6, like_photo=False, follow_photo_user=False)  
```
## go_coment parameters
- **link_photo: str** - url from a instagram photo. 
- **quantity_coments: int** - total of comments in a photo. 
_ **quantity_user_for_coment: int** - quantity of users per comment. 
- **like_photo: bool** - True if you want to leave a like in the photo.  
- **follow_photo_user: bool** - True of you want to follow the photo's owner. 

## Observations
selenium and chromedriver is required  
install selenium - pip install selenium  
download chromedriver - http://chromedriver.chromium.org/downloads  

## Developers
- .
- .
