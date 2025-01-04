#### Flightpath.new

Instantiates a new Flightpath object.

```lua
Flightpath.new(imageFrame: ImageLabel)
```

### Properties

#### Flightpath.Video

The current active video

```lua
Flightpath.Video = {}
```

---

#### Flightpath.Fps

The frame per seconds for the video

```lua
Flightpath.Fps = 60
```

---

#### Flightpath.Looped

Whether the video will loop or not once it goes through all frames

```lua
Flightpath.Looped = false
```

---

#### Flightpath.Playing

Video is playing

```lua
Flightpath.Playing = true
```

---


#### Flightpath.TimeLength

??? warning "Read Only"
    This property is read only.

The time in seconds of the video

```lua
print(Flightpath.TimeLength)
```

---

#### Flightpath.TimePosition

??? warning "Read Only"
    This property is read only.

The time the video is current in

```lua
print(Flightpath.TimePosition)
```

---


### Methods

#### Flightpath:Play()

Plays the current video from the start

```lua
Flightpath:Play()
```

---

#### Flightpath:Pause()

Pauses the video at its current frame

```lua
Flightpath:Pause()
```

---

#### Flightpath:Resume()

Resume the video from its current frame

```lua
Flightpath:Resume()
```

---

#### Flightpath:Stop()

Stop the video and reset to initial time position.

```lua
Flightpath:Stop()
```

---

#### Flightpath:SetTime(time: number)

Set a timestamp to set for the video in seconds.

```lua
Flightpath:SetTime(2) -- Seconds
```

---