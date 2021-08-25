
from .tikzeng import *

#define new block
def block_2ConvPool( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
    to_ConvConvRelu( 
        name="ccr_{}".format( name ),
        s_filer=str(s_filer), 
        n_filer=(n_filer,n_filer), 
        offset=offset, 
        to="({}-east)".format( botton ), 
        width=(size[2],size[2]), 
        height=size[0], 
        depth=size[1],   
        ),    
    to_Pool(         
        name="{}".format( top ), 
        offset="(0,0,0)", 
        to="(ccr_{}-east)".format( name ),  
        width=1,         
        height=size[0] - int(size[0]/4), 
        depth=size[1] - int(size[0]/4), 
        opacity=opacity, ),
    to_connection( 
        "{}".format( botton ), 
        "ccr_{}".format( name )
        )
    ]


def block_Unconv( name, botton, top, s_filer=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_UnPool(  name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(botton),         width=1,              height=size[0],       depth=size[1], opacity=opacity ),
        to_ConvRes( name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),    s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),   s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_ConvRes( name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),       s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1], opacity=opacity ),       
        to_Conv(    name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name), s_filer=str(s_filer), n_filer=str(n_filer), width=size[2], height=size[0], depth=size[1] ),
        to_connection( 
            "{}".format( botton ), 
            "unpool_{}".format( name ) 
            )
    ]




def block_Res( num, name, botton, top, s_filer=256, n_filer=64, offset="(0,0,0)", size=(32,32,3.5), opacity=0.5 ):
    lys = []
    layers = [ *[ '{}_{}'.format(name,i) for i in range(num-1) ], top]
    for name in layers:        
        ly = [ to_Conv( 
            name='{}'.format(name),       
            offset=offset, 
            to="({}-east)".format( botton ),   
            s_filer=str(s_filer), 
            n_filer=str(n_filer), 
            width=size[2],
            height=size[0],
            depth=size[1]
            ),
            to_connection( 
                "{}".format( botton  ), 
                "{}".format( name ) 
                )
            ]
        botton = name
        lys+=ly
    
    lys += [
        to_skip( of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


def block_Encoder( name, botton, top, caption=256, n_filer=64, offset="(1,0,0)", size=(32,32,3.5), maxpool=False, opacity=0.5 ):
    encoder = [];

    if (botton == ""):
        encoder.append(
            to_Conv(
                name="ccr1_{}".format( name ),
                offset=offset, 
                s_filer="",
                to="(0,0,0)",
                n_filer=n_filer, 
                width=size[2],
                height=size[0], 
                depth=size[1],
            )
        );
    else:
        encoder.append(
            to_Conv(
                name="ccr1_{}".format( name ),
                offset=offset, 
                s_filer="",
                n_filer=n_filer, 
                to="({}-east)".format( botton ),
                width=size[2],
                height=size[0], 
                depth=size[1],
            )
        );


    encoder.append(
        to_Conv( 
            name="ccr2_{}".format( name ),
            offset="(0,0,0)", 
            s_filer="",
            caption=caption,
            to="(ccr1_{}-east)".format( name ),
            n_filer=n_filer, 
            width=size[2],
            height=size[0], 
            depth=size[1],
        )
    );
    encoder.append(
        to_ConvRelu( 
            name="ccr3_{}".format( name ),
            offset="(0,0,0)", 
            s_filer="",
            to="(ccr2_{}-east)".format( name ),
            n_filer=n_filer, 
            width=size[2],
            height=size[0], 
            depth=size[1],
        )
    );
    encoder.append(
        to_skip(
            of="ccr1_{}".format( name ),
            to="ccr3_{}".format( name ),
            pos_of=1.25,
        )
    );

    if (maxpool):
        encoder.append(
            to_Pool(         
                name="{}".format( top ), 
                offset="(0,0,0)", 
                caption="",
                to="(ccr3_{}-east)".format( name ),
                width=size[2],   
                height=size[0]//2,
                depth=size[1]//2,
                opacity=opacity
            )
        );

    if (botton != ""):
        encoder.append(
            to_connection( 
                "{}".format( botton ), 
                "ccr1_{}".format( name )
            )
        );

    return encoder;


def block_Decoder( name, botton, top, caption="", n_filer=64, offset="(1,0,0)", size=(32,32,3.5), opacity=0.5 ):
    return [
        to_TransposeConv(
            name='ccr_res_{}'.format(name),
            offset=offset,
            to="({}-east)".format(botton),
            n_filer="",
            s_filer="",
            width=1, 
            height=size[0], 
            depth=size[1]
        ),
        to_Concat(
            name='concate_ccr_res_{}'.format(name),
            offset="(0,0,0)",
            to="(ccr_res_{}-east)".format(name),
            n_filer="",
            s_filer="",
            width=1, 
            height=size[0], 
            depth=size[1],
            opacity=opacity
        ),
        to_Conv( 
            name="ccr1_{}".format( name ),
            offset="(0,0,0)", 
            s_filer="",
            caption="",
            to="(concate_ccr_res_{}-east)".format( name ),
            n_filer=n_filer, 
            width=size[2],
            height=size[0], 
            depth=size[1],
        ),
        to_Conv( 
            name="ccr2_{}".format( name ),
            offset="(0,0,0)", 
            s_filer="",
            caption=caption,
            to="(ccr1_{}-east)".format( name ),
            n_filer=n_filer, 
            width=size[2],
            height=size[0], 
            depth=size[1],
        ),
        to_ConvRelu( 
            name='{}'.format(top),
            offset="(0,0,0)",
            to="(ccr2_{}-east)".format(name),
            s_filer="", 
            caption="",
            n_filer=n_filer,
            width=size[2], 
            height=size[0], 
            depth=size[1],   
        ), 
        to_skip(
            of="ccr1_{}".format( name ),
            to="{}".format( top ),
            pos_of=1.25,
        ),
        to_connection( 
            "{}".format( botton ), 
            "ccr_res_{}".format(name)
            )
    ]

