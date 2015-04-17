/*====================================================================*
 -  Copyright (C) 2001 Leptonica.  All rights reserved.
 -
 -  Redistribution and use in source and binary forms, with or without
 -  modification, are permitted provided that the following conditions
 -  are met:
 -  1. Redistributions of source code must retain the above copyright
 -     notice, this list of conditions and the following disclaimer.
 -  2. Redistributions in binary form must reproduce the above
 -     copyright notice, this list of conditions and the following
 -     disclaimer in the documentation and/or other materials
 -     provided with the distribution.
 -
 -  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 -  ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 -  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 -  A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL ANY
 -  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 -  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 -  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 -  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 -  OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 -  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 -  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *====================================================================*/

/*
 *  colorize_reg.c
 *
 *  This regresstion test demonstrates the detection of red highlight
 *  color in an image, and the generation of a colormapped version
 *  with clean background and colorized highlighting.
 */

#include "allheaders.h"

l_int32 main(int    argc,
             char **argv)
{
l_int32       irval, igval, ibval;
l_float32     rval, gval, bval, fract;
BOXA         *boxa;
FPIX         *fpix;
PIX          *pixs, *pix, *pix1, *pix2, *pix3, *pix4, *pix5, *pix6;
PIX          *pix7, *pix8, *pix9, *pix10, *pix11;
PIXA         *pixa;
L_REGPARAMS  *rp;

    if (regTestSetup(argc, argv, &rp))
              return 1;

    pixa = pixaCreate(0);
    pixs = pixRead("breviar38.150.jpg");
    pixaAddPix(pixa, pixs, L_CLONE);
    regTestWritePixAndCheck(rp, pixs, IFF_JFIF_JPEG);  /* 0 */
    pixDisplayWithTitle(pixs, 0, 0, "Input image", rp->display);

        /* Extract the blue component, which is small in all the text
         * regions, including in the highlight color region */
    pix1 = pixGetRGBComponent(pixs, COLOR_BLUE);
    pixaAddPix(pixa, pix1, L_CLONE);
    regTestWritePixAndCheck(rp, pix1, IFF_JFIF_JPEG);  /* 1 */
    pixDisplayWithTitle(pix1, 200, 0, "Blue component", rp->display);

        /* Do a background normalization, with the background set to
         * approximately 200 */
    pix2 = pixBackgroundNormSimple(pix1, NULL, NULL);
    pixaAddPix(pixa, pix2, L_COPY);
    regTestWritePixAndCheck(rp, pix2, IFF_JFIF_JPEG);  /* 2 */
    pixDisplayWithTitle(pix2, 400, 0, "BG normalized to 200", rp->display);

        /* Do a linear transform on the gray pixels, with 50 going to
         * black and 160 going to white.  50 is sufficiently low to
         * make both the red and black print quite dark.  Quantize
         * to a few equally spaced gray levels.  This is the image
         * to which highlight color will be applied. */
    pixGammaTRC(pix2, pix2, 1.0, 50, 160);
    pix3 = pixThresholdOn8bpp(pix2, 7, 1);
    pixaAddPix(pixa, pix3, L_CLONE);
    regTestWritePixAndCheck(rp, pix3, IFF_JFIF_JPEG);  /* 3 */
    pixDisplayWithTitle(pix3, 600, 0, "Basic quantized with white bg",
                        rp->display);

        /* Identify the regions of red text.  First, make a mask
         * consisting of all pixels such that (R-B)/B is larger
         * than 2.0.  This will have all the red, plus a lot of
         * the dark pixels. */
    fpix = pixComponentFunction(pixs, 1.0, 0.0, -1.0, 0.0, 0.0, 1.0);
    pix4 = fpixThresholdToPix(fpix, 2.0);
    pixInvert(pix4, pix4);  /* red plus some dark text */
    pixaAddPix(pixa, pix4, L_CLONE);
    regTestWritePixAndCheck(rp, pix4, IFF_PNG);  /* 4 */
    pixDisplayWithTitle(pix4, 800, 0, "Red plus dark pixels", rp->display);

        /* Make a mask consisting of all the red and background pixels */
    pix5 = pixGetRGBComponent(pixs, COLOR_RED);
    pix6 = pixThresholdToBinary(pix5, 128);
    pixInvert(pix6, pix6);  /* red plus background (white) */

        /* Intersect the two masks to get a mask consisting of pixels
         * that are almost certainly red.  This is the seed. */
    pix7 = pixAnd(NULL, pix4, pix6);  /* red only (seed) */
    pixaAddPix(pixa, pix7, L_COPY);
    regTestWritePixAndCheck(rp, pix7, IFF_PNG);  /* 5 */
    pixDisplayWithTitle(pix7, 0, 600, "Seed for red color", rp->display);

        /* Make the clipping mask by thresholding the image with
         * the background cleaned to white. */
    pix8 =  pixThresholdToBinary(pix2, 230);  /* mask */
    pixaAddPix(pixa, pix8, L_CLONE);
    regTestWritePixAndCheck(rp, pix8, IFF_PNG);  /* 6 */
    pixDisplayWithTitle(pix8, 200, 600, "Clipping mask for red components",
                        rp->display);

        /* Fill into the mask from the seed */
    pixSeedfillBinary(pix7, pix7, pix8, 8);  /* filled: red plus touching */
    regTestWritePixAndCheck(rp, pix7, IFF_PNG);  /* 7 */
    pixDisplayWithTitle(pix7, 400, 600, "Red component mask filled",
                        rp->display);

        /* Remove long vertical lines from the filled result */
    pix9 = pixMorphSequence(pix7, "o1.40", 0);
    pixSubtract(pix7, pix7, pix9);  /* remove long vertical lines */

        /* Close the regions to be colored  */
    pix10 = pixMorphSequence(pix7, "c5.1", 0);
    pixaAddPix(pixa, pix10, L_CLONE);
    regTestWritePixAndCheck(rp, pix10, IFF_PNG);  /* 8 */
    pixDisplayWithTitle(pix10, 600, 600,
                        "Components defining regions allowing coloring",
                        rp->display);

        /* Get the bounding boxes of the regions to be colored */
    boxa = pixConnCompBB(pix10, 8);

        /* Get a color to paint that is representative of the
         * actual highlight color in the image.  Scale each
         * color component up from the average by an amount necessary
         * to saturate the red.  Then divide the green and
         * blue components by 3.0.  */
    pixGetAverageMaskedRGB(pixs, pix8, 0, 0, 1, L_MEAN_ABSVAL,
                           &rval, &gval, &bval);
    fract = 255.0 / rval;
    irval = lept_roundftoi(fract * rval);
    igval = lept_roundftoi(fract * gval / 3.0);
    ibval = lept_roundftoi(fract * bval / 3.0);
    fprintf(stderr, "(r,g,b) = (%d,%d,%d)\n", irval, igval, ibval);

        /* Color the quantized gray version in the selected regions */
    pix11 = pixColorGrayRegions(pix3, boxa, L_PAINT_DARK, 220, irval,
                                igval, ibval);
    pixaAddPix(pixa, pix11, L_CLONE);
    regTestWritePixAndCheck(rp, pix11, IFF_PNG);  /* 9 */
    pixDisplayWithTitle(pix11, 800, 600, "Final colored result", rp->display);
    pixaAddPix(pixa, pixs, L_CLONE);

        /* Generate a pdf of the intermediate results */
    L_INFO("Writing to /tmp/colorize.pdf\n", rp->testname);
    pixaConvertToPdf(pixa, 90, 1.0, 0, 0, "Colorizing highlighted text",
                     "/tmp/colorize.pdf");

    pixaDestroy(&pixa);
    fpixDestroy(&fpix);
    boxaDestroy(&boxa);
    pixDestroy(&pixs);
    pixDestroy(&pix1);
    pixDestroy(&pix2);
    pixDestroy(&pix3);
    pixDestroy(&pix4);
    pixDestroy(&pix5);
    pixDestroy(&pix6);
    pixDestroy(&pix7);
    pixDestroy(&pix8);
    pixDestroy(&pix9);
    pixDestroy(&pix10);
    pixDestroy(&pix11);
    return regTestCleanup(rp);
}

