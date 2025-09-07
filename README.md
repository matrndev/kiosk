# Self-service Ordering Kiosk

This is a project I set out to do during the summer and winter of 2023. Inspired by the self-service kiosks at fast-food restaurants, I wanted to make a miniature version myself, fully from scratch.

I decided to mainly focus this ordering system for use in cafés, specifically those in hotels, where the payment would be billed to your room. 

Because of the proof-of-concept nature of this project (after all, this was made just to learn and to have fun), this documentation does not fully cover all the necessities required to deploy the application or to build the kiosk itself.

However, if you are interested in this project in any way, would like to build it, make a fork, or if you have any other questions, I’ll be happy to help! Shoot me an e-mail at hello@matrn.dev.

![kiosk photo](https://raw.githubusercontent.com/matrndev/kiosk/refs/heads/main/media/image.jpg)
![3d model image](https://raw.githubusercontent.com/matrndev/kiosk/refs/heads/main/media/3D%20model%201.png)

## Hardware

- Custom 3D printed enclosure (3D models here) 
- Raspberry Pi 4B
- WaveShare Barcode Scanner
- Epson TM-T70 Printer
- Adafruit Nano Thermal Receipt Printer (built into the enclosure; currently unused, replaced by Epson printer)

## Software

- Raspberry Pi OS
- Python (Flask web server)
- HTML + pure JS + Bulma CSS
- MongoDB Atlas database
- Chromium web browser

A single Python script handles everything: the ordering UI, communication with MongoDB, the barcode scanner and thermal printer. The UI is a web application displayed within Chromium in full-screen mode, for seamless navigation.

## Showcase

In the video below I demonstrate the ordering UI, as if a customer were ordering on the kiosk’s display.
<video src='https://github.com/user-attachments/assets/a3f08d1a-9c22-4148-b5c5-0326f5076a9e'>

A receipt printed for the customer:

<img src="https://raw.githubusercontent.com/matrndev/kiosk/refs/heads/main/media/receipt.jpg" alt="receipt image" height="600"/>

Here’s how the kitchen display looks like when a new order is placed. The kitchen display connects to the kiosk over a local network. The kitchen display can be literally anything that runs a web browser -- e.g. mobile phone, tablet, thin client connected to a monitor.
![kitchen display image](https://raw.githubusercontent.com/matrndev/kiosk/refs/heads/main/media/kitchen.png)

## Possible future improvements

- Rewrite of the web app in React (SPA?) for faster loading
- Locally hosted database server
- Admin panel (e.g. for adding items to the menu) -- currently you’re required to manually edit the database, luckily at least MongoDB has a web UI for that
- Make the UI look better :)
- Remove items/edit parts of the order (currently, to remove only a single item from your order, you have to cancel the entire order and start over)
- RFID/barcode identification to ensure the user can only bill their room
