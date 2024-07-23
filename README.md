# CTF

#### The starting file:
![Screenshot 2024-07-23 153923](https://github.com/user-attachments/assets/209d22e4-5f72-404b-a6a6-f4b443f16193)

* In the pulsating heartbeat of 1990s New York City, a shadowy figure known as Hans Gruber's prodigious brother, Simon, emerges as a ruthless mastermind. With a blend of suave charisma and chilling efficiency, he orchestrates a diabolical plot to detonate the city's financial hub. Armed with cunning intellect and a team of skilled mercenaries, Simon Gruber's ambition to rewrite the city's skyline in flames threatens to unleash unparalleled chaos and cement his legacy as a malevolent force to be reckoned with.
* He leaves Detective McClaine a file containing a riddle, but that's not all he left
* With enough digging, he'll notice that the photo embedded in the file is too large for its dimensions, hence, intriguing his curiosity
 

#### Steganography
* Inside the image, McClaine uses a hex editor to read the underlying bytes
* Upon first look, it's a normal JFIF (JPG) image, but it still doesn't explain the large file size
* He first tries looking through the file for anything suspicious, like another photo or file...
![image](https://github.com/user-attachments/assets/a7f4cc2c-1e9c-498a-99a5-3128db340ede)

* After searching enough, he finally lands on an EXE appended to the JPG file, starting with the ubiquitous MZ header
![image](https://github.com/user-attachments/assets/9a97cdfe-a420-4b7a-9ba0-89883c5d37b4)

* Deleting the previous bytes up to the MZ header leaves us with an executable file \
diehard3.exe
  

