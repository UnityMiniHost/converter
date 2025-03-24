# Usage of WeixinGameConverter

1. Run the following command in the main repository to install dependencies:

``` shell
npm install
```

2. Run the converter script like:

``` shell
python ./wx_converter.py -s /path/to/source/folder -t /path/to/target/folder
```

Where:
- `-s` (or `--source`) specifies the path to the source folder.
- `-t` (or `--target`) specifies the path to the target folder.
- `-sp` (or `--subpackage`) specifies whether to package the main and subpackages separately. **[OPTIONAL]**

3. Now we have a `game.zip` in the target folder. Start an http server in the same folder like:

``` shell
npx http-server -g -p 5000
```

4. Then open the demo apk and choose game type `weixinminigame` and input `http://_ip_addr:5000`

