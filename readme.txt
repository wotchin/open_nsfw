
docker resp:
docker pull bvlc/caffe:cpu

docker shell:
docker run -d -p 11001:8888 --volume=$(pwd):/workspace bvlc/caffe:cpu bash ./nsfwd.sh


├── classify_nsfw.py			check
├── nsfw.py				web
├── nsfw_model
│   ├── deploy.prototxt
│   └── resnet_50_1by2_nsfw.caffemodel
├── nsfwd.sh				deamon
├── readme.txt
└── tmp


