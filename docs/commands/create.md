# create
create a Jetstream project

### Command
```sh
jetstream create
```

### Arguments

| Argument         | Input Type       | Description       | Required |
| :----------      | :---------------  | :---------------  |  :---------------  | 
| `-n ` `--name` |  `str`             | Name for the project | Yes |
| `-i ` `--input` |  `str`             | Video to create project (Path or Link) | Yes |
| `-f ` `--fps` |  `int`             | FPS for the video | No |
| `-b ` `--big` |  `bool`             | Big project (Will take longer but prevents ratelimit) | No |