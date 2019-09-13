if [ -d "../$PERSONAL_DIRECTORY" ]; then
	printf "\nError. Director \"$PERSONAL_DIRECTORY\" already exists. \nChange environment variable for PERSONAL_DIRECTORY with: \nexport PERSONAL_DIRECTORY=...\n"
	exit 1
fi
mkdir ../$PERSONAL_DIRECTORY
mkdir ../$PERSONAL_DIRECTORY/task
mkdir ../$PERSONAL_DIRECTORY/project_notes
mkdir ../$PERSONAL_DIRECTORY/track_targets

echo $PERSONAL_DIRECTORY"/" >> ../.gitignore
echo ""
echo "Success!"
echo ""