/**
 * Universal sharing functionality for Tukonect
 * Can be used across different templates
 */

// Generic sharing functions
function shareOnLinkedIn(title, description, url) {
    const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
    window.open(linkedInUrl, '_blank', 'width=600,height=400');
}

function shareOnTwitter(title, description, url, hashtags = []) {
    const text = `${title}${description ? ' - ' + description : ''}`;
    const hashtagString = hashtags.length > 0 ? hashtags.join(',') : 'tukonect';
    
    const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}&hashtags=${encodeURIComponent(hashtagString)}`;
    window.open(twitterUrl, '_blank', 'width=600,height=400');
}

function shareViaEmail(title, description, url, type = 'content') {
    const subject = `${type === 'job' ? 'Job Opportunity' : 'Content'}: ${title}`;
    const body = `Hi,\n\nI found this ${type === 'job' ? 'job opportunity' : 'interesting content'} that might be relevant to you:\n\n${title}${description ? '\n' + description : ''}\n\nCheck it out here: ${url}\n\nBest regards!`;
    
    const emailUrl = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = emailUrl;
}

function copyToClipboard(url, buttonSelector) {
    navigator.clipboard.writeText(url).then(function() {
        // Show success feedback
        const copyBtn = document.querySelector(buttonSelector);
        if (copyBtn) {
            const originalText = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
            copyBtn.classList.remove('btn-outline-secondary');
            copyBtn.classList.add('btn-success');
            
            setTimeout(function() {
                copyBtn.innerHTML = originalText;
                copyBtn.classList.remove('btn-success');
                copyBtn.classList.add('btn-outline-secondary');
            }, 2000);
        }
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        alert('Could not copy link. Please copy manually: ' + url);
    });
}

// Job-specific sharing functions
function shareJobOnLinkedIn() {
    const jobTitle = document.querySelector('[data-job-title]')?.getAttribute('data-job-title') || 'Job Opportunity';
    const company = document.querySelector('[data-company]')?.getAttribute('data-company') || '';
    const url = window.location.href;
    const description = company ? `at ${company}` : '';
    
    shareOnLinkedIn(jobTitle, description, url);
}

function shareJobOnTwitter() {
    const jobTitle = document.querySelector('[data-job-title]')?.getAttribute('data-job-title') || 'Job Opportunity';
    const company = document.querySelector('[data-company]')?.getAttribute('data-company') || '';
    const url = window.location.href;
    const description = company ? `at ${company} on Tukonect` : 'on Tukonect';
    
    shareOnTwitter(jobTitle, description, url, ['jobs', 'career', 'tukonect']);
}

function shareJobViaEmail() {
    const jobTitle = document.querySelector('[data-job-title]')?.getAttribute('data-job-title') || 'Job Opportunity';
    const company = document.querySelector('[data-company]')?.getAttribute('data-company') || '';
    const url = window.location.href;
    const description = company ? `at ${company}` : '';
    
    shareViaEmail(jobTitle, description, url, 'job');
}

function copyJobLink() {
    const url = window.location.href;
    copyToClipboard(url, 'a[onclick="copyJobLink()"]');
}

// Forum-specific sharing functions
function shareForumOnLinkedIn() {
    const forumTitle = document.querySelector('[data-forum-title]')?.getAttribute('data-forum-title') || 'Forum Discussion';
    const author = document.querySelector('[data-author]')?.getAttribute('data-author') || '';
    const url = window.location.href;
    const description = author ? `by ${author}` : '';
    
    shareOnLinkedIn(forumTitle, description, url);
}

function shareForumOnTwitter() {
    const forumTitle = document.querySelector('[data-forum-title]')?.getAttribute('data-forum-title') || 'Forum Discussion';
    const author = document.querySelector('[data-author]')?.getAttribute('data-author') || '';
    const url = window.location.href;
    const description = author ? `by ${author} on Tukonect` : 'on Tukonect';
    
    shareOnTwitter(forumTitle, description, url, ['discussion', 'tukonect', 'community']);
}

function shareForumViaEmail() {
    const forumTitle = document.querySelector('[data-forum-title]')?.getAttribute('data-forum-title') || 'Forum Discussion';
    const author = document.querySelector('[data-author]')?.getAttribute('data-author') || '';
    const url = window.location.href;
    const description = author ? `by ${author}` : '';
    
    shareViaEmail(forumTitle, description, url, 'discussion');
}

function copyForumLink() {
    const url = window.location.href;
    copyToClipboard(url, 'a[onclick="copyForumLink()"]');
}

// Event-specific sharing functions
function shareEventOnLinkedIn() {
    const eventTitle = document.querySelector('[data-event-title]')?.getAttribute('data-event-title') || 'Event';
    const eventDate = document.querySelector('[data-event-date]')?.getAttribute('data-event-date') || '';
    const url = window.location.href;
    const description = eventDate ? `on ${eventDate}` : '';
    
    shareOnLinkedIn(eventTitle, description, url);
}

function shareEventOnTwitter() {
    const eventTitle = document.querySelector('[data-event-title]')?.getAttribute('data-event-title') || 'Event';
    const eventDate = document.querySelector('[data-event-date]')?.getAttribute('data-event-date') || '';
    const url = window.location.href;
    const description = eventDate ? `on ${eventDate} - Join us!` : 'Join us!';
    
    shareOnTwitter(eventTitle, description, url, ['event', 'networking', 'tukonect']);
}

function shareEventViaEmail() {
    const eventTitle = document.querySelector('[data-event-title]')?.getAttribute('data-event-title') || 'Event';
    const eventDate = document.querySelector('[data-event-date]')?.getAttribute('data-event-date') || '';
    const url = window.location.href;
    const description = eventDate ? `on ${eventDate}` : '';
    
    shareViaEmail(eventTitle, description, url, 'event');
}

function copyEventLink() {
    const url = window.location.href;
    copyToClipboard(url, 'a[onclick="copyEventLink()"]');
}

// Initialize sharing functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add click effects to all share buttons
    const shareButtons = document.querySelectorAll('a[onclick*="share"], button[onclick*="share"]');
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add a small delay to show the click effect
            this.style.opacity = '0.7';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 200);
        });
    });
    
    // Add hover effects
    shareButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
            this.style.transition = 'all 0.2s ease';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
