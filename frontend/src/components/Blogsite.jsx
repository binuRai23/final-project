import React from 'react';
import { useNavigate } from 'react-router-dom';

function Blogsite() {
  const navigate = useNavigate();

  const handleTextFieldClick = () => {
    navigate('/create-post');
  };

  return (
    <div style={styles.dashboardContainer}>
      <div style={styles.mainContent}>
        <h1>StudyBuddy</h1>
        <div style={styles.searchSection}>
          <input
            type="text"
            placeholder="Click here to create a post"
            style={styles.textField}
            onClick={handleTextFieldClick}
          />
        </div>
      </div>
    </div>
  );
}

const styles = {
    dashboardContainer: {
      display: 'flex',
      height: '100vh',
    },
    sidebar: {
      width: '20%',
      background: '#3b82f6',
      color: 'white',
      padding: '1rem',
    },
    mainContent: {
      width: '80%',
      padding: '2rem',
      background: '#f5f5f5',
    },
    searchSection: {
      marginTop: '2rem',
    },
    textField: {
      width: '100%',
      padding: '0.5rem',
      fontSize: '1rem',
      borderRadius: '4px',
      border: '1px solid #ccc',
    },
  };

export default Blogsite;
