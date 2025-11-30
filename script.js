

// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', () => {
    const submitButton = document.querySelector('button[type="submit"]');
    const journalEntry = document.getElementById('journalEntry');
    const stressInput = document.getElementById('stress');
    const moodsSelect = document.getElementById('moods');

    // Load previous entries from localStorage
    const entries = JSON.parse(localStorage.getItem('journalEntries')) || [];

    submitButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default form submission

        const entry = journalEntry.value.trim();
        const stress = stressInput.value.trim();
        const mood = moodsSelect.value;

        // Simple validation
        if (!entry) {
            alert('Please write something in your journal entry.');
            return;
        }
        if (!stress) {
            alert('Please enter your stress level.');
            return;
        }

        // Create a journal object
        const journalObject = {
            date: new Date().toLocaleString(),
            entry,
            stress,
            mood
        };

        // Save entry to localStorage
        entries.push(journalObject);
        localStorage.setItem('journalEntries', JSON.stringify(entries));

        // Clear form
        journalEntry.value = '';
        stressInput.value = '';
        moodsSelect.selectedIndex = 0;

        // Feedback
        alert('Journal entry saved! Check console for details.');

        // Log the entry
        console.log('New Journal Entry:', journalObject);
    });
});
