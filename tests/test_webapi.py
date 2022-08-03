# -*- encoding: utf-8 -*-

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from browse.models import FormatSpecification, Entity, Quantity, DataFile, Release, Account


TEST_ACCOUNT_EMAIL = "test@localhost"
TEST_ACCOUNT_USER = "test_user"


def _create_test_user_and_authenticate(client):
    test_user = Account.objects.create(email=TEST_ACCOUNT_EMAIL, username=TEST_ACCOUNT_USER)
    client.force_authenticate(user=test_user)


def create_format_spec(client, document_ref):
    "Create a FormatSpecification object and return the response"

    url = reverse("formatspecification-list")

    response = client.post(
        url,
        format="json",
        data={
            "document_ref": document_ref,
            "title": "My dummy document",
            "file_mime_type": "application/text",
        },
    )
    return response


def create_entity_spec(client, name, parent=None):
    "Create a Entity object and return the response"

    url = reverse("entity-list")

    response = client.post(
        url, format="json", data={"name": name, "parent": parent, "quantities": []}
    )
    return response


def create_quantity_spec(client, name, entity, format_spec, data_files=[]):
    "Create a Quantity object and return the response"

    url = reverse("quantity-list")

    response = client.post(
        url,
        format="json",
        data={
            "name": name,
            "parent_entity": entity,
            "format_spec": format_spec,
            "data_files": data_files,
        },
    )
    return response


def create_data_file_spec(
    client, name, metadata, quantity, spec_version="1.0", release_tags=[]
):
    "Create a DataFile object and return the response"

    url = reverse("datafile-list")

    response = client.post(
        url,
        format="json",
        data={
            "name": name,
            "metadata": metadata,
            "quantity": quantity,
            "spec_version": spec_version,
            "release_tags": release_tags,
        },
    )
    return response


def create_release_spec(client, tag, comment="", data_files=[]):
    "Create a DataFile object and return the response"

    url = reverse("release-list")

    response = client.post(
        url,
        format="json",
        data={
            "tag": tag,
            "comment": comment,
            "data_files": data_files,
        },
    )
    return response


class FormatSpecificationTests(APITestCase):
    def test_create_format_spec(self):
        """
        Ensure we can create a new FormatSpecification object.
        """

        _create_test_user_and_authenticate(self.client)

        response = create_format_spec(self.client, "DUMMY_REF_001")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FormatSpecification.objects.count(), 1)
        self.assertEqual(
            FormatSpecification.objects.get().document_ref, "DUMMY_REF_001"
        )


class EntityTests(APITestCase):
    def test_create_entity(self):
        """
        Ensure we can create a new quantity object.
        """

        _create_test_user_and_authenticate(self.client)

        response = create_entity_spec(self.client, "test_entity")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entity.objects.count(), 1)
        self.assertEqual(Entity.objects.get().name, "test_entity")


class QuantityTests(APITestCase):
    def setUp(self):
        _create_test_user_and_authenticate(self.client)

        self.formatspec_response = create_format_spec(self.client, "DUMMY_REF_001")
        self.entity_response = create_entity_spec(self.client, "test_entity")

    def test_create_quantity(self):
        """
        Ensure we can create a new quantity object.
        """

        response = create_quantity_spec(
            self.client,
            name="test_quantity",
            entity=self.entity_response.json()["url"],
            format_spec=self.formatspec_response.json()["url"],
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quantity.objects.count(), 1)
        self.assertEqual(Quantity.objects.get().name, "test_quantity")


class DataFileTests(APITestCase):
    def setUp(self):
        _create_test_user_and_authenticate(self.client)

        self.formatspec_response = create_format_spec(self.client, "DUMMY_REF_001")
        self.entity_response = create_entity_spec(self.client, "test_entity")
        self.quantity_response = create_quantity_spec(
            self.client,
            name="test_quantity",
            entity=self.entity_response.json()["url"],
            format_spec=self.formatspec_response.json()["url"],
        )

    def test_create_datafile(self):
        """
        Ensure we can create a new DataFile object.
        """
        response = create_data_file_spec(
            self.client,
            name="test_datafile",
            metadata={"a": 10, "b": "hello"},
            quantity=self.quantity_response.json()["url"],
        )

        # Check the result of the POST call
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataFile.objects.count(), 1)
        self.assertEqual(DataFile.objects.get().name, "test_datafile")

        # Now get the object from the database and check that
        # everything looks ok
        response = self.client.get(response.json()["url"])
        json = response.json()

        assert "quantity" in json
        self.assertEqual(json["quantity"], self.quantity_response.json()["url"])

        assert "metadata" in json
        self.assertEqual(json["metadata"]["a"], 10)
        self.assertEqual(json["metadata"]["b"], "hello")


class ReleaseTests(APITestCase):
    def setUp(self):
        _create_test_user_and_authenticate(self.client)
        
        self.formatspec_response = create_format_spec(self.client, "DUMMY_REF_001")
        self.entity_response = create_entity_spec(self.client, "test_entity")
        self.quantity_response = create_quantity_spec(
            self.client,
            name="test_quantity",
            entity=self.entity_response.json()["url"],
            format_spec=self.formatspec_response.json()["url"],
        )
        self.datafile_response = create_data_file_spec(
            self.client,
            name="test_datafile",
            metadata={"a": 10, "b": "hello"},
            quantity=self.quantity_response.json()["url"],
        )

    def test_create_release(self):
        """
        Ensure we can create a new Release object.
        """
        response = create_release_spec(self.client, "v1.0")

        # Check the result of the POST call
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Release.objects.count(), 1)
        self.assertEqual(Release.objects.get().tag, "v1.0")

        # Add a datafile to the release
        rel_url = response.json()["url"]
        response = self.client.patch(
            rel_url,
            format="json",
            data={
                "tag": "v1.0",
                "comment": "",
                "data_files": [self.datafile_response.json()["url"]],
            },
        )
        response = self.client.get(rel_url)
        json = response.json()
        self.assertEqual(json["tag"], "v1.0")
        self.assertEqual(len(json["data_files"]), 1)

        # Try to access the data file through the release tag
        response = self.client.get(
            "/releases/v1.0/test_entity/test_quantity/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        assert response.url in self.datafile_response.json()["url"]
