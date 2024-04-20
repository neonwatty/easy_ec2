import sys
from easy_ec2.router import Router


def main(*args):
    # unapck args
    pargs = {}
    # check if args is empty
    if not args:
        # check if sys.argv is empty
        if len(sys.argv) > 1:
            pargs = sys.argv
        else:
            print('args and sys.argv is empty!')
            sys.exit(1)
    else:
        pargs = args

    # create app instance
    app = Router(pargs)
    return app.run()


if __name__ == "__main__":
    # unpack command line args
    args = {}
    if len(sys.argv) > 1:
        args = dict(enumerate(sys.argv))
    else:
        print('sys.argv is empty!')
        sys.exit(1)

    # run main
    main(**args)
