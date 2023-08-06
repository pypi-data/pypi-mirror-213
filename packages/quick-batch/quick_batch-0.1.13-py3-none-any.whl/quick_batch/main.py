import sys
import fire
import runner
import manual_scaler


def main(config=None):
    # check config - used as script fire will not be used
    if not config:
        # check argument provided - config or num_processors
        if sys.argv[1] == 'config':
            config = sys.argv[2]
            runner.run(config)
            return None
        elif sys.argv[1] == 'scale':
            num_processors = int(sys.argv[2])
            manual_scaler.scaler(num_processors)
            return None

    # check config - used as script fire will be used
    runner.run(config)
    return None


if __name__ == '__main__':
    fire.Fire(main)
