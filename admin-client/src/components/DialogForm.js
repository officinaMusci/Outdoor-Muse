import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  Box,
  DialogActions,
  Button
} from '@mui/material';


/**
 * Renders a dialog containing a custom form
 * @property  {boolean}           open         If the dialog is open
 * @property  {CallableFunction}  setOpen      The function to call to toggle the open status of the dialog
 * @property  {CallableFunction}  onCancel     The function to call on form cancel
 * @property  {CallableFunction}  onValidate   The function to call on form validation
 * @property  {CallableFunction}  onSubmit     The function to call on form submit
 * @property  {string}            title        The dialog title
 * @property  {string}            description  The dialog description
 * @property  {Array}             children     The form to render
 * @component
 */
const DialogForm = props => {
  const {
    open,
    setOpen,
    onCancel,
    onValidate,
    onSubmit,
    title,
    description,
    children
  } = props;

  const handleCancel = () => {
    if (onCancel) {
      onCancel();
    }
    setOpen(false);
  };

  const handleSubmit = () => {
    if (onValidate) {
      if (onValidate()) {
        if (onSubmit) {
          onSubmit();
        }
        setOpen(false);
      }
    } else {
      if (onSubmit) {
        onSubmit();
      }
      setOpen(false);
    }
  };

  return (
    <Dialog
      fullWidth
      maxWidth='xs'
      open={open}
      onClose={handleCancel}
    >
      {title ?
        <DialogTitle>
          {title}
        </DialogTitle>
        :
        null
      }
      <DialogContent dividers>
        {description ? 
          <DialogContentText>
            {description}
          </DialogContentText>
          :
          null
        }
        <Box
          component='form'
          sx={{
            mb: 1.5,
            display: 'flex',
            justifyContent: 'center',
            flexDirection: 'column',
            '& > .MuiBox-root': {
              display: 'flex',
              justifyContent: 'center',
              flexDirection: 'row',
              gap: 1
            }
          }}
          noValidate
          autoComplete='off'
          onSubmit={e => {
            e.preventDefault();
            handleSubmit();
          }}
        >
          {children}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCancel}>Annuler</Button>
        <Button onClick={handleSubmit}>Soumettre</Button>
      </DialogActions>
    </Dialog>
  )
}

export default DialogForm;