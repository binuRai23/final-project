import React from 'react';

function Post() {
  return (
    <div style={styles.container}>
      <h1>StudyBuddy</h1>
      <p>Create post and help priors</p>
      <textarea
        placeholder="Write your post here"
        style={styles.textArea}
      ></textarea>
      <button style={styles.button}>Upload Video</button>
      <button style={styles.button}>Upload File</button>
      <select style={styles.select}>
        <option>Select Category</option>
      </select>
      <button style={styles.postButton}>Post</button>
    </div>
  );
}

const styles = {
    pageContainer: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: '#f5f5f5',
    },
    container: {
      width: '50%',
      background: '#ffffff',
      padding: '2rem',
      textAlign: 'center',
      borderRadius: '10px',
      boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
    },
    title: {
      fontSize: '2rem',
      color: '#3b82f6',
      marginBottom: '1rem',
    },
    subtitle: {
      marginBottom: '1.5rem',
      fontSize: '1.2rem',
      color: '#555',
    },
    textArea: {
      width: '100%',
      height: '100px',
      marginBottom: '1rem',
      padding: '0.8rem',
      borderRadius: '4px',
      border: '1px solid #ccc',
    },
    buttonGroup: {
      display: 'flex',
      justifyContent: 'space-between',
      marginBottom: '1rem',
    },
    button: {
      padding: '0.5rem 1rem',
      background: '#3b82f6',
      color: '#ffffff',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    select: {
      width: '100%',
      padding: '0.8rem',
      marginBottom: '1rem',
      borderRadius: '4px',
      border: '1px solid #ccc',
    },
    postButton: {
      padding: '0.8rem 1.5rem',
      background: '#3b82f6',
      color: '#ffffff',
      border: 'none',
      borderRadius: '4px',
      fontSize: '1rem',
      cursor: 'pointer',
    },
  };
export default Post;
