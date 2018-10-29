from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from iot.factories import DeviceFactory, TypeFactory


class PingTestCase(APITestCase):
    def test_index_pages(self):
        url = reverse('ping')
        response = self.client.get(url)

        self.assertEqual(
            status.HTTP_200_OK, response.status_code, 'Wrong response code for {}'.format(url)
        )


class DeviceTestCase(APITestCase):
    def test_list(self):
        url = reverse('device-list')
        response = self.client.get(url)

        self.assertEqual(
            status.HTTP_200_OK, response.status_code, 'Wrong response code for {}'.format(url)
        )

        data = response.json()

        self.assertEqual(0, data['count'])
        self.assertEqual(0, len(data['results']))
        self.assertIsNone(data['_links']['next']['href'])
        self.assertIsNone(data['_links']['previous']['href'])

    def test_list_1_item(self):
        device = DeviceFactory.create()

        url = reverse('device-list')
        response = self.client.get(url)

        self.assertEqual(
            status.HTTP_200_OK, response.status_code, 'Wrong response code for {}'.format(url)
        )

        data = response.json()

        self.assertEqual(1, data['count'])
        self.assertEqual(1, len(data['results']))

        self.assertEqual(device.reference, data['results'][0]['reference'])
        self.assertEqual(device.application, data['results'][0]['application'])
        self.assertEqual(len(device.categories.split(',')), len(data['results'][0]['categories']))
        self.assertAlmostEqual(float(device.location.longitude),
                               float(data['results'][0]['longitude']))
        self.assertAlmostEqual(float(device.location.latitude),
                               float(data['results'][0]['latitude']))
        self.assertEqual(device.address.street, data['results'][0]['address']['street'])
        self.assertEqual(device.address.postal_code, data['results'][0]['address']['postal_code'])
        self.assertEqual(device.address.city, data['results'][0]['address']['city'])
        self.assertEqual(device.owner.organisation, data['results'][0]['organisation'])

    def test_list_pagination(self):
        DeviceFactory.create_batch(8)
        DeviceFactory.create(location=None)
        t = TypeFactory.create()
        DeviceFactory.create(types=[t, ])

        url = '{}?page_size=5'.format(reverse('device-list'))
        response = self.client.get(url)

        self.assertEqual(
            status.HTTP_200_OK, response.status_code, 'Wrong response code for {}'.format(url)
        )

        data = response.json()

        self.assertEqual(10, data['count'])
        self.assertEqual(5, len(data['results']))

        self.assertIsNotNone(data['_links']['next']['href'])
        self.assertIsNone(data['_links']['previous']['href'])

        response = self.client.get(data['_links']['next']['href'])

        self.assertEqual(
            status.HTTP_200_OK, response.status_code, 'Wrong response code for {}'.format(url)
        )

        data = response.json()

        self.assertEqual(10, data['count'])
        self.assertEqual(5, len(data['results']))

        self.assertIsNone(data['_links']['next']['href'])
        self.assertIsNotNone(data['_links']['previous']['href'])

    def test_detail(self):
        device = DeviceFactory.create()

        url = reverse('device-detail', kwargs={'pk': device.pk})
        response = self.client.get(url)

        self.assertEqual(
            status.HTTP_200_OK, response.status_code, 'Wrong response code for {}'.format(url)
        )

        data = response.json()

        self.assertEqual(device.reference, data['reference'])
        self.assertEqual(device.application, data['application'])
        self.assertEqual(len(device.categories.split(',')), len(data['categories']))
        self.assertAlmostEqual(float(device.location.longitude), float(data['longitude']))
        self.assertAlmostEqual(float(device.location.latitude), float(data['latitude']))
        self.assertEqual(device.address.street, data['address']['street'])
        self.assertEqual(device.address.postal_code, data['address']['postal_code'])
        self.assertEqual(device.address.city, data['address']['city'])
        self.assertEqual(device.owner.organisation, data['organisation'])

    def test_put(self):
        device = DeviceFactory.create()

        url = reverse('device-detail', kwargs={'pk': device.pk})
        response = self.client.put(url, data={})

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_post(self):
        device = DeviceFactory.create()

        url = reverse('device-detail', kwargs={'pk': device.pk})
        response = self.client.put(url, data={})

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    def test_delete(self):
        device = DeviceFactory.create()

        url = reverse('device-detail', kwargs={'pk': device.pk})
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
