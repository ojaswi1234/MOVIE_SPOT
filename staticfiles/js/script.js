// JavaScript (in a .js file or <script> tag in your Django template)
document.addEventListener('DOMContentLoaded', () => {
  const aiBtn = document.querySelector('#ai-btn');
  if (!aiBtn) return;

  const openModal = () => {
    const body = document.querySelector('body');
    body.style.overflow = 'hidden';

    // Create backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center transition-opacity duration-500';
    backdrop.setAttribute('aria-hidden', 'true');

    // Create modal
    const aiDiv = document.createElement('div');
    aiDiv.className = 'w-full max-w-md md:max-w-2xl h-fit bg-gradient-to-tr from-cyan-200 to-lime-200 rounded-lg flex flex-col justify-center items-center relative shadow-2xl p-6   overflow-y-visible';
    aiDiv.setAttribute('role', 'dialog');
    aiDiv.setAttribute('aria-labelledby', 'ai-modal-title');
    aiDiv.innerHTML = `
    <h2 id="ai-modal-title" class="text-2xl font-bold mb-4">AI Movie Recommendations</h2>
    <button 
        class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl" 
        aria-label="Close AI recommendations modal"
      >
        &times;
      </button>
    <p class="text-center mb-4">Get personalized movie recommendations based on your preferences.(Choose any of these)</p>

    <form action="/movies/ai-recommendations/" method="POST" class=" text-black ">

    <div id="genre-titles" class="flex flex-wrap justify-center mb-4 gap-y-2">
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer ">
            <span class="mr-2 text-black">Action</span>
            <input type="checkbox" name="genre" value="Action" class="absolute w-fit h-fit opacity-0">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Comedy</span>
            <input type="checkbox" name="genre" value="Comedy" class="absolute w-fit h-fit  opacity-0">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Drama</span>
            <input type="checkbox" name="genre" value="Drama" class="absolute w-fit h-fit  opacity-0">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Horror</span>
            <input type="checkbox" name="genre" value="Horror" class="absolute w-fit h-fit  opacity-0">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Romance</span>
            <input type="checkbox" name="genre" value="Romance" class="absolute w-fit h-fit  opacity-0 ">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Sci-Fi</span>
            <input type="checkbox" name="genre" value="Sci-Fi" class="absolute w-fit h-fit  opacity-0">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Thriller</span>
            <input type="checkbox" name="genre" value="Thriller" class="absolute w-fit h-fit  opacity-0 ">
        </label>
        <label class="flex items-center mr-4 p-3 rounded-full border-2 border-gray-400 cursor-pointer">
            <span class="mr-2">Fantasy</span>
            <input type="checkbox" name="genre" value="Fantasy" class="absolute w-fit h-fit  opacity-0">
        </label>

   
    </form>
    </div>
    <div class=" mb-4">
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors">
        Get Recommendations
      </button>
    </div>

      <div class="bg-white w-full h-fit mt-4 p-4 rounded-lg shadow-lg"></div>
    <p class="text-sm text-gray-500 mt-4">Click outside the modal or press ESC to close.</p>
    
      
    
    `;

    // Add modal to backdrop
    backdrop.appendChild(aiDiv);
    body.appendChild(backdrop);

    // Focus on the modal for accessibility
    aiDiv.focus();

    // Close modal functionality
    const closeBtn = aiDiv.querySelector('button');
    const closeModal = () => {
      body.style.overflow = '';
      backdrop.remove();
      aiBtn.focus(); // Return focus to the trigger button
    };

    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) closeModal();
    });

    // ESC key to close
    const escHandler = (e) => {
      if (e.key === 'Escape') closeModal();
    };
    document.addEventListener('keydown', escHandler);

    // Focus trap
    const focusableElements = aiDiv.querySelectorAll('button, [href]');
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    aiDiv.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable.focus();
        } else if (!e.shiftKey && document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable.focus();
        }
      }
    });

    // Cleanup event listeners when modal is closed
    backdrop.dataset.listeners = JSON.stringify({ escHandler });
  };

  aiBtn.addEventListener('click', openModal);


 
   

});
