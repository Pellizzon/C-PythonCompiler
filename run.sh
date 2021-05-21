FILE=""
if [ $# -eq 0 ]; then
    read -p "enter path to program file: " FILE
else
    FILE="$1"
fi
    
python3 main.py $FILE
nasm -f elf32 -F dwarf -g output/out.asm
ld -m elf_i386 -o output/out output/out.o 
./output/out