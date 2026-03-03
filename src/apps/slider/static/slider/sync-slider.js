/**
 * SyncSlider
 *
 * Synchronized Slick slider component.
 *
 * Features:
 * - Custom event API
 * - Public access to internal state
 *
 * Options:
 * {
 *   parentClass: string,
 *   autoInit: boolean,
 *   events: {
 *     imageClicked: Function
 *   }
 * }
 *
 * Public API:
 * - init()
 * - destroy()
 * - getState()
 */
function SyncSlider(options) {
  const defaultOptions = {
    parentClass: '.slider',
    autoInit: true,
    events: {},
  };

  const settings = $.extend(true, {}, defaultOptions, options);

  const state = {
    initialized: false,
    $container: null,
    $previewSlider: null,
    $navigationSlider: null,
  };

  if (settings.autoInit) {
    init();
  }

  /**
   * Initializes component
   */
  function init() {
    if (state.initialized) return;

    if (!findElements()) return;

    createSlider(state.$previewSlider, {
      asNavFor: settings.parentClass + ' .slider-block__navigation',
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      draggable: false,
      fade: true,
      lazyLoad: 'ondemand',
    });

    createSlider(state.$navigationSlider, {
      asNavFor: settings.parentClass + ' .slider-block__preview',
      slidesToShow: 5,
      focusOnSelect: true,
      centerMode: true,
      centerPadding: '0px',
      responsive: [
        {
          breakpoint: 992,
          settings: {
            arrows: false,
            centerPadding: '40px',
            slidesToShow: 3
          }
        },
      ],
      prevArrow: $(`${settings.parentClass} .slider-block__btn-prev`),
      nextArrow: $(`${settings.parentClass} .slider-block__btn-next`),
    });

    bindEvents();

    state.initialized = true;
  }

  /**
   * Finds required DOM elements
   */
  function findElements() {
    state.$container = $(settings.parentClass);

    if (!state.$container.length) {
      console.warn(`Container not found: ${settings.parentClass}`);
      return false;
    }

    state.$previewSlider = state.$container.find('.slider-block__preview');
    state.$navigationSlider = state.$container.find('.slider-block__navigation');

    if (!state.$previewSlider.length) {
      console.warn('.slider-block__preview not found');
      return false;
    }

    return true;
  }

  /**
   * Initializes slick instance
   */
  function createSlider($el, options) {
    if (!$el || !$el.length) return;
    $el.slick(options);
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
   * Destroys slick instances
   */
  function destroy() {
    if (!state.initialized) return;

    if (state.$previewSlider) {
      state.$previewSlider.slick('unslick');
    }

    if (state.$navigationSlider) {
      state.$navigationSlider.slick('unslick');
    }

    state.initialized = false;
  }

  /**
   * Binds internal DOM events
   */
  function bindEvents() {
    state.$previewSlider.on('click', 'img', function (e) {
      const src = $(this).attr('src');

      emit('imageClicked', {
        src: src,
        originalEvent: e,
      });
    });
  }

  /**
   * Emits component event
   */
  function emit(eventName, payload) {
    if (
      settings.events &&
      typeof settings.events[eventName] === 'function'
    ) {
      settings.events[eventName]({
        type: eventName,
        sliderName: state.name,
        detail: payload,
      });
    }
  }

  return {
    init,
    destroy,
    getState,
  };
}

