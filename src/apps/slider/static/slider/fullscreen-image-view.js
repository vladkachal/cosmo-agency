/**
 * FullscreenImageView
 *
 * Standalone fullscreen viewer component.
 *
 * Features:
 * - Zoomist support
 * - Public access to internal state
 *
 * Options:
 * {
 *   overlaySelector: string,
 *   imageSelector: string,
 *   closeSelector: string,
 *   autoInit: boolean,
 *   enableZoom: boolean
 * }
 *
 * Public API:
 * - init()
 * - show(src)
 * - hide()
 * - getState()
 */
function FullscreenImageView(options) {
  const defaultOptions = {
    overlaySelector: '.fullscreen-image-view',
    imageSelector: 'img',
    closeSelector: '.fullscreen-image-view__close',
    autoInit: true,
    enableZoom: true,
  };

  const settings = $.extend({}, defaultOptions, options);

  const state = {
    initialized: false,
    overlay: null,
    image: null,
    zoomInstance: null,
  };

  if (settings.autoInit) {
    init();
  }

  /**
   * Initializes component
   */
  function init() {
    if (state.initialized || !findElements()) return;
    bindEvents();
    state.initialized = true;
  }

  /**
   * Finds required DOM elements
   */
  function findElements() {
    state.overlay = $(settings.overlaySelector);

    if (!state.overlay.length) {
      console.warn('Fullscreen overlay not found');
      return false;
    }

    state.image = state.overlay.find(settings.imageSelector);

    return state.image.length > 0;
  }

  /**
   * Shows fullscreen image
   */
  function show(src) {
    if (!src) return;

    state.image.attr('src', src);
    state.overlay.addClass('fullscreen-image-view--active');

    if (settings.enableZoom && !state.zoomInstance) {
      state.zoomInstance = new Zoomist('.fullscreen-image-view__container', {
        zoomer: true,
        smooth: true,
      });
    }
  }

  /**
   * Hides fullscreen
   */
  function hide() {
    state.overlay.removeClass('fullscreen-image-view--active');
  }

  /**
   * Returns internal state and settings
   */
  function getState() {
    return {
      options: settings,
      state: state,
    };
  }

  /**
   * Binds DOM events
   */
  function bindEvents() {
    state.overlay.on('click', settings.closeSelector, function (e) {
      if (e.target !== this) return;
      hide();
    });
  }

  return {
    getState,
    init,
    show,
    hide,
  };
}
