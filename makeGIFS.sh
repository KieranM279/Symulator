
# Bash script to run all the Gifs I want and then collate them into another folder


# Go to Generation 0 and make gif there
echo "Making generation 0 gif"
cd /home/ubuntu/Symulator_corner_large/frames/Generation0/
bash makegif.sh
mv *.gif ../../gifs/

# Go to Generattion 50 and make gif there
echo "Making generation 50 gif"
cd /home/ubuntu/Symulator_corner/frames_large/Generation50/
bash makegif.sh
mv *.gif ../../gifs/

# Go to Generation 100 and make gif there
echo "Making generation 100 gif"
cd /home/ubuntu/Symulator_corner/frames_large/Generation100/
bash makegif.sh
mv *.gif ../../gifs/

# Go to Generation 500 and make gif there
echo "Making generation 500 gif"
cd /home/ubuntu/Symulator_corner/frames_large/Generation500/
bash makegif.sh
mv *.gif ../../gifs/
