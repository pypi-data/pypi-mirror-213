from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

PROPER_IMG = "proper.jpeg"
TOO_LARGE_IMG = "too_large.jpeg"
UNSUPPORTED_TYPE_IMG = "unsupported_type.png"


def test_Uploaded_File_Goes_Through():
    """
    Would upload file to "upload_file_first"
    Upload File is jpeg, and size less than 12000 bytes
    """
    with open(f"test/img/{PROPER_IMG}", "rb") as img:
        response = client.post(
            "/upload/first",
            files={"file": (PROPER_IMG, img, "image/jpeg")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == PROPER_IMG
    assert data["content_type"] == "image/jpeg"


def test_Uploaded_File_Is_Too_Large_Size():
    """
    Would upload file to "upload_file_first"
    Upload File is jpeg, and size more than 12000 bytes
    """
    with open(f"test/img/{TOO_LARGE_IMG}", "rb") as img:
        response = client.post(
            "/upload/first",
            files={"file": (TOO_LARGE_IMG, img, "image/jpeg")}
        )

    assert response.status_code == 413
    assert response.reason == "Request Entity Too Large"


def test_Uploaded_File_Is_Unsupported_File_Type():
    """
    Would upload file to "upload_file_first"
    Upload File is png, and size less than 12000 bytes
    """
    with open(f"test/img/{UNSUPPORTED_TYPE_IMG}", "rb") as img:
        response = client.post(
            "/upload/first",
            files={"file": (UNSUPPORTED_TYPE_IMG, img, "image/png")}
        )

    assert response.status_code == 415
    assert response.reason == "Unsupported Media Type"


def test_When_No_Specified_In_App_Path_Uploaded_File_Goes_Through_Even_In_The_Case_Of_Too_Large_Size():
    """
    Would upload file to "upload_file_second"
    Upload File is jpeg, and size more than 12000 bytes
    """
    with open(f"test/img/{TOO_LARGE_IMG}", "rb") as img:
        response = client.post(
            "/upload/second",
            files={"file": (TOO_LARGE_IMG, img, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == TOO_LARGE_IMG
    assert data["content_type"] == "image/jpeg"


def test_When_No_Specified_In_App_Path_Uploaded_File_Goes_Through_Even_In_The_Case_Of_Unsupported_File_Type():
    """
    Would upload file to "upload_file_second"
    Upload File is png, and size less than 12000 bytes
    """
    with open(f"test/img/{UNSUPPORTED_TYPE_IMG}", "rb") as img:
        response = client.post(
            "/upload/second",
            files={"file": (UNSUPPORTED_TYPE_IMG, img, "image/png")}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == UNSUPPORTED_TYPE_IMG
    assert data["content_type"] == "image/png"

