file =  open('data.txt','r')

pack_number = 1
item_count  = 1

f = open('pack1.txt','a')

for lines in file :


        if(item_count == 0 or item_count == 101):
            pack_number = pack_number+1
            f = open('pack'+ str(pack_number) + '.txt   ', 'a')
            item_count = 1


        f.write(lines)
        item_count = item_count + 1