document.addEventListener('DOMContentLoaded', function() {
  // Toggle mobile navigation
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function() {
      navLinks.classList.toggle('show');
    });
  }
  
  // Flag submission
  const flagForm = document.getElementById('flag-form');
  const flagResult = document.getElementById('flag-result');
  
  if (flagForm) {
    flagForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const challengeId = this.dataset.challengeId;
      const flagInput = document.getElementById('flag-input');
      const submitBtn = document.getElementById('submit-flag');
      const attemptsEl = document.getElementById('attempts-count');
      
      if (!flagInput.value.trim()) {
        showResultMessage('Please enter a flag', 'error');
        return;
      }
      
      // Disable the submit button while processing
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Checking...';
      
      // Submit the flag
      fetch(`/challenges/submit/${challengeId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          'flag': flagInput.value
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          showResultMessage(data.message, 'success');
          
          // Update UI to show completion
          const challengeCard = document.querySelector(`.challenge-card[data-id="${challengeId}"]`);
          if (challengeCard) {
            challengeCard.classList.add('completed');
            const statusBadge = challengeCard.querySelector('.status-badge');
            if (statusBadge) {
              statusBadge.innerHTML = 'Completed';
              statusBadge.className = 'badge badge-success status-badge';
            }
          }
          
          // If there's a next challenge, show button to navigate there
          if (data.next_challenge) {
            const nextBtn = document.createElement('a');
            nextBtn.href = `/challenges/${data.next_challenge}`;
            nextBtn.className = 'btn btn-primary mt-3';
            nextBtn.innerHTML = 'Next Challenge';
            flagResult.appendChild(nextBtn);
          }
          
          // Disable the form
          flagInput.disabled = true;
          submitBtn.disabled = true;
          submitBtn.innerHTML = 'Completed';
          
        } else {
          showResultMessage(data.message, 'error');
          
          // Update attempts counter
          if (attemptsEl && data.attempts) {
            attemptsEl.textContent = data.attempts;
          }
          
          // Reset the submit button
          submitBtn.disabled = false;
          submitBtn.innerHTML = 'Submit Flag';
        }
      })
      .catch(error => {
        console.error('Error:', error);
        showResultMessage('An error occurred. Please try again.', 'error');
        
        // Reset the submit button
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Submit Flag';
      });
    });
  }
  
  // Function to show result messages
  function showResultMessage(message, type) {
    if (!flagResult) return;
    
    // Remove previous messages
    const prevMessage = flagResult.querySelector('.alert');
    if (prevMessage) {
      prevMessage.remove();
    }
    
    // Create and add new message
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} fade-in`;
    alertDiv.innerHTML = message;
    
    flagResult.prepend(alertDiv);
    
    // Auto-remove after 5 seconds if it's an error
    if (type === 'error') {
      setTimeout(() => {
        alertDiv.remove();
      }, 5000);
    }
  }
  
  // Hint buttons
  const hintButtons = document.querySelectorAll('.hint-btn');
  
  hintButtons.forEach(btn => {
    btn.addEventListener('click', function() {
      const challengeId = this.dataset.challengeId;
      const hintContainer = document.getElementById(`hint-${challengeId}`);
      
      if (!hintContainer) return;
      
      // If hint is already loaded, just toggle visibility
      if (hintContainer.dataset.loaded === 'true') {
        hintContainer.classList.toggle('d-none');
        return;
      }
      
      // Otherwise, fetch the hint
      fetch(`/challenges/hint/${challengeId}`)
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            hintContainer.innerHTML = `<div class="alert alert-info">${data.hint}</div>`;
            hintContainer.dataset.loaded = 'true';
            hintContainer.classList.remove('d-none');
          } else {
            hintContainer.innerHTML = `<div class="alert alert-warning">${data.message}</div>`;
            hintContainer.classList.remove('d-none');
          }
        })
        .catch(error => {
          console.error('Error:', error);
          hintContainer.innerHTML = '<div class="alert alert-danger">An error occurred while loading the hint.</div>';
          hintContainer.classList.remove('d-none');
        });
    });
  });
  
  // Terminal effect
  const terminalElements = document.querySelectorAll('.terminal-animation');
  
  terminalElements.forEach(terminal => {
    const text = terminal.dataset.text || '';
    const speed = parseInt(terminal.dataset.speed) || 50;
    let i = 0;
    
    terminal.innerHTML = '<span class="terminal-cursor">_</span>';
    
    const typeEffect = () => {
      if (i < text.length) {
        if (terminal.childNodes[0].nodeType === Node.TEXT_NODE) {
          terminal.childNodes[0].nodeValue += text.charAt(i);
        } else {
          terminal.insertBefore(document.createTextNode(text.charAt(i)), terminal.childNodes[0]);
        }
        i++;
        setTimeout(typeEffect, speed);
      }
    };
    
    setTimeout(typeEffect, 1000);
  });

  // Challenge page specific scripts
  const currentPath = window.location.pathname;
  
  // Flag 7: JavaScript obfuscation challenge
  if (currentPath.includes('/challenges/7')) {
    // This is intentionally obfuscated as part of the challenge
    const _0x5837=['toString','charCodeAt','30494GJGlBD','1cVQyJf','1qQANQi','2JHyYGO','241254mCQtZa','flag','1642695FMLJgn','value','flag-input','getElementById','9RaQDVe','18939seBluJ','3QzKGLO','1217799CCmfBa','96738DKvloH','14sCtpMg','The\x20real\x20flag\x20is:\x20','10GjXFcH'];const _0x40b2=function(_0x10c854,_0xc3e71c){_0x10c854=_0x10c854-0x147;let _0x583740=_0x5837[_0x10c854];return _0x583740;};(function(_0x28e0f0,_0x5f57db){const _0x1db359=_0x40b2;while(!![]){try{const _0x509b3b=parseInt(_0x1db359(0x14b))*parseInt(_0x1db359(0x156))+parseInt(_0x1db359(0x14f))*-parseInt(_0x1db359(0x157))+parseInt(_0x1db359(0x153))*parseInt(_0x1db359(0x15a))+parseInt(_0x1db359(0x150))*-parseInt(_0x1db359(0x14a))+parseInt(_0x1db359(0x149))*parseInt(_0x1db359(0x14d))+parseInt(_0x1db359(0x155))*parseInt(_0x1db359(0x147))+parseInt(_0x1db359(0x14e))*parseInt(_0x1db359(0x152));if(_0x509b3b===_0x5f57db)break;else _0x28e0f0['push'](_0x28e0f0['shift']());}catch(_0x4dfae7){_0x28e0f0['push'](_0x28e0f0['shift']());}}}(_0x5837,0x89f23));const checkFlag7=()=>{const _0x258c14=_0x40b2,_0x22e2db=document[_0x258c14(0x14c)](_0x258c14(0x14b)),_0x2be5d1='FoundtheObfuscatedFlag';if(_0x22e2db[_0x258c14(0x14a)]===_0x2be5d1)console['log'](_0x258c14(0x154)+_0x2be5d1);else{let _0x11f20e='';for(let _0x2dc012=0x0;_0x2dc012<_0x2be5d1['length'];_0x2dc012++){_0x11f20e+=String['fromCharCode'](_0x2be5d1[_0x258c14(0x158)](_0x2dc012)+0x1);}document[_0x258c14(0x14c)](_0x258c14(0x14b))[_0x258c14(0x14a)]=_0x11f20e;}};window[_0x40b2(0x159)]=checkFlag7;
  }
  
  // Flag 4: XSS challenge
  if (currentPath.includes('/challenges/4')) {
    const commentForm = document.getElementById('comment-form');
    const commentsSection = document.getElementById('comments-section');
    
    if (commentForm) {
      commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const commentInput = document.getElementById('comment-input');
        const comment = commentInput.value.trim();
        
        if (!comment) return;
        
        // Add the comment to the page (intentionally vulnerable)
        const commentDiv = document.createElement('div');
        commentDiv.className = 'card mb-3';
        commentDiv.innerHTML = `
          <div class="card-body">
            <h5 class="card-title">Anonymous User</h5>
            <p class="card-text">${comment}</p>
            <small class="text-muted">Just now</small>
          </div>
        `;
        
        commentsSection.prepend(commentDiv);
        commentInput.value = '';
        
        // Check if this might be an XSS attempt
        if (comment.includes('<script>') && comment.includes('alert(')) {
          // This is intentional for the challenge - simulating an XSS vulnerability
          setTimeout(() => {
            try {
              // Very simplified XSS check - in a real app, this would be handled properly
              // This is intentionally vulnerable for the CTF challenge
              const scriptContent = comment.match(/<script>(.*?)<\/script>/i)[1];
              if (scriptContent.includes('alert(') && scriptContent.includes('flag')) {
                const flagInput = document.getElementById('flag-input');
                if (flagInput) {
                  flagInput.value = 'XSSAlertFlagFound';
                  document.querySelector('#flag-form button[type="submit"]').click();
                }
              }
            } catch (error) {
              console.error('Error in XSS simulation:', error);
            }
          }, 500);
        }
      });
    }
  }
});
