//import { useState, useRef } from "react";
import UsersApi from "../../api/UsersApi";
import { Loading } from "../../components/utils/Loading";
import ErrorCard from "../../components/utils/ErrorCard";

export function DisplayPic({ user }) {
    const image= null;
  //const [image, setImage] = useState(null);
  /*
  const fileInput = useRef();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
    /*
  // Open file picker
  //const openFilePicker = () => fileInput.current.click();


  // Handle file selection
  const handleFileSelected = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setImage(URL.createObjectURL(file));
    setError("");
    setSuccess("");
  };

  // Upload cropped image
  const handleUpload = async () => {
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      // Use percentage-based crop to prevent overzoom
      const file = fileInput.current.files[0];
      const blob = file; 
 
      const formData = new FormData();
      formData.append("file", blob, "profile.jpg");

      await UsersApi.changedp(user.uid, formData);
      setSuccess("Profile image updated successfully!");
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.message || "Updating user failed. Try again."
      );
    } finally {
      setLoading(false);
      setImage(null); // close cropper
    }
  };
  */

  return (
    <div>
        {/* 
      {error && <ErrorCard message={error} />}
      {success && <div className="alert alert-success">{success}</div>}
      {loading && <Loading />}
            */}
      <div className="row mb-3">
        <label className="col-md-4 col-lg-3 col-form-label">Profile Image</label>
        <div className="col-md-8 col-lg-9">
          {image ? (
            <img
            src={image}
            alt="Profile"
            style={{ maxWidth: "300px", height: "300px" }}
          />
          ) : (
            <img
              src={user.display_pic}
              alt="Profile"
              style={{ maxWidth: "300px", height: "300px" }}
            />
          )}

          <div className="pt-2">
          { /*
            { <label>For better experience use 300x300 resolution</label><br ></br>  }
            <input
              type="file"
              ref={fileInput}
              style={{ display: "none" }}
              accept="image/*"
              onChange={handleFileSelected}
            />

            <button
              className="btn btn-primary btn-sm"
              style={{ marginRight: "5px" }}
              title="Select new profile image"
              onClick={openFilePicker}
            >
              <i className="bi bi-image-fill"></i>
            </button>

            {image && (
              <button
                type="button"
                className="btn btn-success btn-sm"
                onClick={handleUpload}
                style={{ marginRight: "5px" }}
                title="Upload new profile image"
              >
                <i className="bi bi-upload"></i>
              </button>
            )}

            <button
              className="btn btn-danger btn-sm"
              title="Remove my profile image"
            >
              <i className="bi bi-trash"></i>
            </button>
            */
            }
          </div>
        </div>
      </div>
    </div>
  );
}
