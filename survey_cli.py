#!/usr/bin/env python3
"""
Command-line interface for the Survey Filler
"""

import argparse
import logging
import sys
from pathlib import Path

from survey_filler import SurveyFiller
from survey_filler.config import SurveyConfig


def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Override any existing configuration
    )


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Automated Survey Filler for platforms like freecash.com',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fill a survey with default settings
  python survey_cli.py https://example.com/survey

  # Use custom configuration
  python survey_cli.py https://example.com/survey -c config/my_config.yaml

  # Run in headless mode
  python survey_cli.py https://example.com/survey --headless

  # Verbose output
  python survey_cli.py https://example.com/survey -v
        """
    )

    parser.add_argument(
        'url',
        help='Survey URL to fill out'
    )

    parser.add_argument(
        '-c', '--config',
        help='Path to configuration YAML file',
        default=None
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode'
    )

    parser.add_argument(
        '-m', '--max-pages',
        type=int,
        default=20,
        help='Maximum number of pages to fill (default: 20)'
    )

    parser.add_argument(
        '-s', '--strategy',
        choices=['random', 'first', 'middle', 'last'],
        default='random',
        help='Selection strategy for multiple choice questions'
    )

    parser.add_argument(
        '--screenshot',
        help='Save screenshot after completion (filename)',
        default=None
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Load or create configuration
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Configuration file not found: {args.config}", file=sys.stderr)
            return 1
        config = SurveyConfig.from_yaml(args.config)
    else:
        config = SurveyConfig(selection_strategy=args.strategy)

    print(f"🤖 Starting Survey Filler")
    print(f"📋 Survey URL: {args.url}")
    print(f"⚙️  Strategy: {config.selection_strategy}")
    print(f"🌐 Headless: {args.headless}")
    print()

    try:
        # Create and run survey filler
        with SurveyFiller(config=config, headless=args.headless) as filler:
            success = filler.fill_survey(args.url, max_pages=args.max_pages)

            if success:
                print()
                print("✅ Survey completed successfully!")
                
                # Take screenshot if requested
                if args.screenshot:
                    filler.take_screenshot(args.screenshot)
                    print(f"📸 Screenshot saved: {args.screenshot}")
            else:
                print()
                print("⚠️  Survey filling incomplete or failed")
                return 1

    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
