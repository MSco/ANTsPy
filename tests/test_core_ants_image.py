"""
Test ants_image.py

nptest.assert_allclose
self.assertEqual
self.assertTrue

"""

import os
import unittest
from common import run_tests
from context import ants
from tempfile import mktemp

import numpy as np
import numpy.testing as nptest

import ants


class TestClass_ANTsImage(unittest.TestCase):
    """
    Test ants.ANTsImage class
    """
    def setUp(self):
        img2d = ants.image_read(ants.get_ants_data('r16')).clone('float')
        img3d = ants.image_read(ants.get_ants_data('mni')).clone('float')
        self.imgs = [img2d, img3d]
        self.pixeltypes = ['unsigned char', 'unsigned int', 'float']

    def tearDown(self):
        pass

    def test_get_spacing(self):
        self.setUp()
        for img in self.imgs:
            spacing = img.spacing
            self.assertTrue(isinstance(spacing, tuple))
            self.assertEqual(len(img.spacing), img.dimension)

    def test_set_spacing(self):
        self.setUp()
        for img in self.imgs:
            # set spacing from list
            new_spacing_list = [6.9]*img.dimension
            img.set_spacing(new_spacing_list)
            self.assertEqual(img.spacing, tuple(new_spacing_list))

            # set spacing from tuple
            new_spacing_tuple = tuple(new_spacing_list)
            img.set_spacing(new_spacing_tuple)
            self.assertEqual(img.spacing, new_spacing_tuple)

    def test_get_origin(self):
        self.setUp()
        for img in self.imgs:
            origin = img.origin
            self.assertTrue(isinstance(origin, tuple))
            self.assertEqual(len(img.origin), img.dimension)

    def test_set_origin(self):
        for img in self.imgs:
            # set spacing from list
            new_origin_list = [6.9]*img.dimension
            img.set_origin(new_origin_list)
            self.assertEqual(img.origin, tuple(new_origin_list))

            # set spacing from tuple
            new_origin_tuple = tuple(new_origin_list)
            img.set_origin(new_origin_tuple)
            self.assertEqual(img.origin, new_origin_tuple)

    def test_get_direction(self):
        self.setUp()
        for img in self.imgs:
            direction = img.direction
            self.assertTrue(isinstance(direction,np.ndarray))
            self.assertTrue(img.direction.shape, (img.dimension,img.dimension))

    def test_set_direction(self):
        self.setUp()
        for img in self.imgs:
            new_direction = np.eye(img.dimension)*3
            img.set_direction(new_direction)
            nptest.assert_allclose(img.direction, new_direction)

    def test_view(self):
        self.setUp()
        for img in self.imgs:
            myview = img.view()
            self.assertTrue(isinstance(myview, np.ndarray))
            self.assertEqual(myview.shape, img.shape)

            # test that changes to view are direct changes to the image
            myview *= 3.
            nptest.assert_allclose(myview, img.numpy())

    def test_numpy(self):
        self.setUp()
        for img in self.imgs:
            mynumpy = img.numpy()
            self.assertTrue(isinstance(mynumpy, np.ndarray))
            self.assertEqual(mynumpy.shape, img.shape)

            # test that changes to view are NOT direct changes to the image
            mynumpy *= 3.
            nptest.assert_allclose(mynumpy, img.numpy()*3.)

    def test_clone(self):
        self.setUp()
        for img in self.imgs:
            orig_ptype = img.pixeltype
            for ptype in self.pixeltypes:
                imgclone = img.clone(ptype)

                self.assertEqual(imgclone.pixeltype, ptype)
                self.assertEqual(img.pixeltype, orig_ptype)
                # test physical space consistency
                self.assertTrue(ants.image_physical_space_consistency(img, imgclone))
                if ptype == orig_ptype:
                    # test that they dont share image pointer
                    view1 = img.view()
                    view1 *= 6.9
                    nptest.assert_allclose(view1, imgclone.numpy()*6.9)

    def test_new_image_like(self):
        self.setUp()
        for img in self.imgs:
            myarray = img.numpy()
            myarray *= 6.9
            imgnew = img.new_image_like(myarray)
            # test physical space consistency
            self.assertTrue(ants.image_physical_space_consistency(img, imgnew))
            # test data
            nptest.assert_allclose(myarray, imgnew.numpy())
            nptest.assert_allclose(myarray, img.numpy()*6.9)

    def test_to_file(self):
        self.setUp()
        for img in self.imgs:
            filename = mktemp(suffix='.nii.gz')
            img.to_file(filename)
            # test that file now exists
            self.assertTrue(os.path.exists(filename))
            img2 = ants.image_read(filename)
            # test physical space and data
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img.numpy(), img2.numpy())

            try:
                os.remove(filename)
            except:
                pass

    def test_apply(self):
        self.setUp()
        for img in self.imgs:
            img2 = img.apply(lambda x: x*6.9)
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), img.numpy()*6.9)

    def test__add__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img + 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), img.numpy()+6.9)

    def test__sub__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img - 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), img.numpy()-6.9)

    def test__mul__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img * 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), img.numpy()*6.9)

    def test__div__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img / 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), img.numpy()/6.9)

    def test__pow__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img ** 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), img.numpy()**6.9)

    def test__gt__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img > 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), (img.numpy()>6.9).astype('int'))

    def test__ge__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img >= 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), (img.numpy()>=6.9).astype('int'))

    def test__lt__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img < 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), (img.numpy()<6.9).astype('int'))

    def test__le__(self):
        self.setUp()
        for img in self.imgs:
            img2 = img <= 6.9
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), (img.numpy()<=6.9).astype('int'))

    def test__eq__(self):
        self.setUp()
        for img in self.imgs:
            img2 = (img == 6.9)
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), (img.numpy()==6.9).astype('int'))

    def test__ne__(self):
        self.setUp()
        for img in self.imgs:
            img2 = (img != 6.9)
            self.assertTrue(ants.image_physical_space_consistency(img, img2))
            nptest.assert_allclose(img2.numpy(), (img.numpy()!=6.9).astype('int'))

    def test__getitem__(self):
        self.setUp()
        for img in self.imgs:
            if img.dimension == 2:
                img2 = img[6:9,6:9]
                nptest.assert_allclose(img2, img.numpy()[6:9,6:9])
            elif img.dimension == 3:
                img2 = img[6:9,6:9,6:9]
                nptest.assert_allclose(img2, img.numpy()[6:9,6:9,6:9])

    def test__setitem__(self):
        self.setUp()
        for img in self.imgs:
            if img.dimension == 2:
                img[6:9,6:9] = 6.9
                self.assertTrue(img.numpy()[6:9,6:9].mean(), 6.9)
            elif img.dimension == 3:
                img[6:9,6:9,6:9] = 6.9
                self.assertTrue(img.numpy()[6:9,6:9,6:9].mean(), 6.9)


class TestModule_ants_image(unittest.TestCase):

    def setUp(self):
        img2d = ants.image_read(ants.get_ants_data('r16')).clone('float')
        img3d = ants.image_read(ants.get_ants_data('mni')).clone('float')
        self.imgs = [img2d, img3d]
        self.pixeltypes = ['unsigned char', 'unsigned int', 'float']

    def tearDown(self):
        pass

    def test_copy_image_info(self):
        for img in self.imgs:
            img2 = img.clone()
            img2.set_spacing([6.9]*img.dimension)
            img2.set_origin([6.9]*img.dimension)
            self.assertTrue(not ants.image_physical_space_consistency(img,img2))

            img3 = ants.copy_image_info(reference=img, target=img2)
            self.assertTrue(ants.image_physical_space_consistency(img,img3))

    def test_get_spacing(self):
        for img in self.imgs:
            spacing = ants.get_spacing(img)
            self.assertTrue(isinstance(spacing, tuple))
            self.assertEqual(len(ants.get_spacing(img)), img.dimension)

    def test_set_spacing(self):
        for img in self.imgs:
            # set spacing from list
            new_spacing_list = [6.9]*img.dimension
            ants.set_spacing(img, new_spacing_list)
            self.assertEqual(img.spacing, tuple(new_spacing_list))

            # set spacing from tuple
            new_spacing_tuple = tuple(new_spacing_list)
            ants.set_spacing(img, new_spacing_tuple)
            self.assertEqual(ants.get_spacing(img), new_spacing_tuple)

    def test_get_origin(self):
        for img in self.imgs:
            origin = ants.get_origin(img)
            self.assertTrue(isinstance(origin, tuple))
            self.assertEqual(len(ants.get_origin(img)), img.dimension)

    def test_set_origin(self):
        for img in self.imgs:
            # set spacing from list
            new_origin_list = [6.9]*img.dimension
            ants.set_origin(img, new_origin_list)
            self.assertEqual(img.origin, tuple(new_origin_list))

            # set spacing from tuple
            new_origin_tuple = tuple(new_origin_list)
            ants.set_origin(img, new_origin_tuple)
            self.assertEqual(ants.get_origin(img), new_origin_tuple)

    def test_get_direction(self):
        for img in self.imgs:
            direction = ants.get_direction(img)
            self.assertTrue(isinstance(direction,np.ndarray))
            self.assertTrue(ants.get_direction(img).shape, (img.dimension,img.dimension))

    def test_set_direction(self):
        for img in self.imgs:
            new_direction = np.eye(img.dimension)*3
            ants.set_direction(img, new_direction)
            nptest.assert_allclose(ants.get_direction(img), new_direction)

    def test_image_physical_spacing_consistency(self):
        for img in self.imgs:
            self.assertTrue(ants.image_physical_space_consistency(img,img))
            self.assertTrue(ants.image_physical_space_consistency(img,img,datatype=True))
            clonetype = 'float' if img.pixeltype != 'float' else 'unsigned int'
            img2 = img.clone(clonetype)
            self.assertTrue(ants.image_physical_space_consistency(img,img2))
            self.assertTrue(not ants.image_physical_space_consistency(img,img2,datatype=True))

    def test_image_type_cast(self):
        # test with list of images
        imgs2 = ants.image_type_cast(self.imgs)
        for img in imgs2:
            self.assertTrue(img.pixeltype, 'float')

    def test_allclose(self):
        for img in self.imgs:
            img2 = img.clone()
            self.assertTrue(ants.allclose(img,img2))
            self.assertTrue(ants.allclose(img*6.9, img2*6.9))
            self.assertTrue(not ants.allclose(img, img2*6.9))


if __name__ == '__main__':
    run_tests()
