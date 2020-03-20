# remove index
sed -i 's/^[0-9]*//g' $1

#remove metadata
sed -i '/^#/d' $1

#remove lines that contain DBLQ (contain NaNs)
sed 's/DBLQ//g' $1

#remove tag in the beginning of line
sed -i 's/^\t*//g' $1 

cp $1 $2

