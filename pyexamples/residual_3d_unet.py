import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( '../brain-images/t1.png', to='(-4.5,0,0)', name="t1", opacity=0.6),
    to_input( '../brain-images/t1ce.png', to='(-4.0,0,0)', name="t1ce", opacity=0.6),
    to_input( '../brain-images/t2.png', to='(-3.5,0,0)', name="t2", opacity=0.6),
    to_input( '../brain-images/flair.png', to='(-3.0,0,0)', name="flair-east", opacity=0.6),
    *block_Encoder("b1", "", "pool_b1", caption="(120$\\times$120$\\times$80)", n_filer=64, offset="(1,0,0)", size=(40,40,2), maxpool=True, opacity=0.5),
    *block_Encoder("b2", "pool_b1", "pool_b2", caption="(60$\\times$60$\\times$40)", n_filer=128, offset="(2.5,0,0)", size=(20,20,4), maxpool=True, opacity=0.5),
    *block_Encoder("b3", "pool_b2", "pool_b3", caption="(30$\\times$30$\\times$20)", n_filer=256, offset="(2,0,0)", size=(10,10,8), maxpool=True, opacity=0.5),
    *block_Encoder("b4", "pool_b3", "ccr_res_b6", caption="(15$\\times$15$\\times$10)", n_filer=512, offset="(1,0,0)", size=(5,5,16), maxpool=False, opacity=0.5),
    
    #Decoder
    *block_Decoder( name="b6", botton="ccr3_b4", top='end_b6', caption="(30$\\times$30$\\times$20)",  n_filer=256, offset="(1,0,0)", size=(10,10,8), opacity=0.5 ),
    to_skip( of='ccr3_b3', to='ccr_res_b6', pos_of=1.25),
    *block_Decoder( name="b7", botton="end_b6", top='end_b7', caption="(60$\\times$60$\\times$40)", n_filer=128, offset="(2,0,0)", size=(20,20,4), opacity=0.5 ),
    to_skip( of='ccr3_b2', to='ccr_res_b7', pos_of=1.25),
    *block_Decoder( name="b8", botton="end_b7", top='end_b8', caption="(120$\\times$120$\\times$80)", n_filer=64, offset="(2.5,0,0)", size=(40,40,2), opacity=0.5 ),
    to_skip( of='ccr3_b1', to='ccr_res_b8', pos_of=1.25),
    to_Conv( "end_conv", offset="(2.5,0,0)", to="(end_b8-east)", s_filer="", n_filer=1, width=2, height=40, depth=40),
    to_connection(
        "end_b8",
        "end_conv",
    ),
    to_output( '../brain-images/seg.png', to='end_conv', xshift=2.5),
    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
