# VTM_CTU_partition
Save and Dispaly VTM CTU partition info.

**Johnny_1280x720_60_0.yuv, Johnny_1280x720_60_VTM.h266 and CTU/CTU_x.txt** is only used for test. 

This Project Usage:
```
First, install numpy, PIL, matplotlib for your Python3.

And then:
git clone https://github.com/codec2021/VTM_CTU_partition.git

python3 Draw_CTU_Partition.py

You will get the result picture:
```
<img width="996" alt="image" src="https://github.com/codec2021/VTM_CTU_partition/assets/13790178/7bea13b7-30b7-4025-80a7-6f1197ed5cbf">


## Step1. Change VTM22.0 Encoder Code

VTM Code: https://vcgit.hhi.fraunhofer.de/jvet/VVCSoftware_VTM.git

At the end of function **void EncCu::compressCtu**, please add:

```c++
std::string ctuNum = std::to_string(ctuRsAddr);
std::ofstream ctuPartitionFile;

std::cout << ctuNum << std::endl;
ctuPartitionFile.open("./CTU_" + ctuNum + ".txt");

for (auto &currCU : cs.traverseCUs(CS::getArea(cs, area, ChannelType::LUMA), ChannelType::LUMA))
{
	const CompArea&  lumaArea = currCU.block(COMPONENT_Y);
	int cuX = lumaArea.x;
	int cuY = lumaArea.y;
	int cuH = lumaArea.height;
	int cuW = lumaArea.width;
	std::string cuInfo = "";

	cuInfo = std::to_string(cuX) + " " + std::to_string(cuY) + " " + std::to_string(cuH) + " " + std::to_string(cuW) +"\n";
	ctuPartitionFile << cuInfo;
}
ctuPartitionFile.close();
```

## Step2. run VTM Encoder
for example:
```shell
./EncoderApp -c ./encoder_randomaccess_vtm.cfg -i Johnny_1280x720_60.yuv -wdt 1280 -hgt 720 -fr 30 -f 1 -q 30 -b Johnny_1280x720_60_VTM.h266
```
## Step3. move all CTU_x.txt file to local ./CTU Dir
<img width="1347" alt="image" src="https://github.com/codec2021/VTM_CTU_partition/assets/13790178/60fd7d6c-5c6b-42a5-adb6-f60f44e070f0">



## Step4. run the Draw_CTU_Partition.py by python3
set the encoded yuv name, width, height, ctu_size:
<img width="841" alt="image" src="https://github.com/codec2021/VTM_CTU_partition/assets/13790178/2ca13dcf-75d7-4a4d-a705-5ea7142c9606">



and then run:
```shell
python3 Draw_CTU_Partition.py
```
