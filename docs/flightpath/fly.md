Now that you have Flightpath in your game, lets go to the movies and learn to fly with Flightpath!

Create a `LocalScript` in `StarterGui` and enter the following code:

```lua title="myVideoManager.luau"
local Flightpath = require(path/to/Flightstream)

local myVideo = require(path/to/video)

local screenGui = Instance.new("ScreenGui", game.Player.LocalPlayer.PlayerGui)
local imageLabel = Instance.new("ImageLabel", screenGui)

screenGui.IgnoreGuiInset = true
imageLabel.Size = UDim2.fromScale(1,1)

local video = Flightpath.new(imageLabel)
video.Video = myVideo
video.Looped = true

print("My video started playing")
video:Play()

task.wait(5)

print("Paused on frame")
video:Pause()

task.wait(2)

print("Resumed on stopped frame")
video:Resume()

task.wait(2)

print("Stopped video")
video:Stop()

video:SetTime(0.2) -- You can see how many seconds the video is in total using video.TimeLength
```

In this code block we imported the Flightpath module and create a new Instance of it passing our    `ImageLabel`.

Once you instantiate a new Flightpath you can control this video similarly to Roblox's VideoFrame. It's API is made to resemble it closely.

