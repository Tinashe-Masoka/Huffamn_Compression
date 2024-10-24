from stat import UF_COMPRESSED
import bitio
import huffman
import pickle


def read_tree(tree_stream):
  data = pickle.load(tree_stream)
  return data



def decode_byte(tree, bitreader):

  fake_tree = tree

  while True :

    if isinstance( fake_tree , huffman.TreeLeaf) :
      return fake_tree.getValue()

    bit = bitreader.readbit()

    if bit == 0 :
        fake_tree = fake_tree.getLeft()
    
    if bit == 1 :
        fake_tree = fake_tree.getRight() 


def decompress(compressed, uncompressed):

  tree = read_tree(compressed)

  
  mybitreader = bitio.BitReader(compressed)


  mybitwriter = bitio.BitWriter(uncompressed)

  
  while True :
    byte = decode_byte(tree , mybitreader)
    if byte == None : break
    mybitwriter.writebits(byte , 8)
  mybitwriter.flush()






def write_tree(tree, tree_stream):
  pickle.dump( tree , tree_stream , 4)
        


def compress(tree, uncompressed, compressed):

  write_tree(tree , compressed)
  
  table = huffman.make_encoding_table(tree)


  mybitreader = bitio.BitReader(uncompressed)


  mybitwriter = bitio.BitWriter(compressed)
  end_of_file = False
  while not end_of_file:
    try:
      
      byte = mybitreader.readbits(8)

      for i in table[byte] :
        mybitwriter.writebit(i)

    except EOFError:
      
      for i in table[None] :
        mybitwriter.writebit(i)
      mybitwriter.flush()
      end_of_file = True
      pass

