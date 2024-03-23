# VTM_CTU_partition
Save and Dispaly VTM CTU partition info.

This Project Usage:
```
git clone
python3 Draw_CTU_Partition.py
```

## Step1. Change VTM22.0 Encoder Code
At the end of function **void EncCu::compressCtu**, please add:

```c++
std::string filename = std::to_string(ctuRsAddr);
std::ofstream myfile;

std::cout << filename << std::endl;
myfile.open("./CTU_" + filename + ".txt");

for (auto &currCU : cs.traverseCUs(CS::getArea(cs, area, ChannelType::LUMA), ChannelType::LUMA))
{
  const CompArea&  lumaArea = currCU.block(COMPONENT_Y);
	int cuX = lumaArea.x;
	int cuY = lumaArea.y;
	int cuH = lumaArea.height;
	int cuW = lumaArea.width;
	std::string info = "";

  info = std::to_string(cuX) + " " + std::to_string(cuY) + " " + std::to_string(cuH) +" "+ std::to_string(cuW) +"\n";
	myfile << info;
}
myfile.close();
```

## Step2. run VTM Encoder
for example:
```shell
./EncoderApp -c ./encoder_randomaccess_vtm.cfg -i Johnny_1280x720_60.yuv -wdt 1280 -hgt 720 -fr 30 -f 1 -q 30 -b Johnny_1280x720_60_VTM.h266
```
## Step3. move all CTU_x.txt to local CTU Dir
<img width="1347" alt="image" src="https://github.com/codec2021/VTM_CTU_partition/assets/13790178/60fd7d6c-5c6b-42a5-adb6-f60f44e070f0">



## Step4. run the Draw_CTU_Partition.py by python3
set the encoded yuv name, width, height, ctu_size:
<img width="794" alt="image" src="https://github.com/codec2021/VTM_CTU_partition/assets/13790178/79d4f724-65a5-437c-ad79-eaab09a71a8e">


and then run:
```shell
python3 Draw_CTU_Partition.py
```
